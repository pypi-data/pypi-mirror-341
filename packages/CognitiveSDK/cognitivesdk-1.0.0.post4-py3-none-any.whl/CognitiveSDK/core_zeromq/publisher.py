import asyncio
import zmq
import zmq.asyncio
import numpy as np
import json
import time
from typing import Optional
from ..utils.logger import logger
from ..utils.shared_state import SharedState
from ..utils.ports import PortManager

class Publisher:
    """
    Optimized ZeroMQ PUB for real-time EEG data publishing.
    
    This publisher is optimized for:
    1. Low latency - using binary data serialization
    2. Limited HWM - to avoid buffer bloat
    3. Timestamps - to track data freshness
    """
    def __init__(self, topic: str, name: str):
        self.topic = topic
        self.name = name
        self.ctx = zmq.asyncio.Context.instance()
        self.pub_socket = self.ctx.socket(zmq.PUB)
        
        self.stopped = False
        self.paused = False  # Default state depends on control mode
        self._first_publish = True
        self._msg_counter = 0  # Message sequence counter
        self._first_publish_timestamp = None # Timestamp of the first publish event
        
        # Command handling
        self.command_socket = None
        self._command_task = None
        self._control_enabled = False
        
        try:
            # Get shared state instance
            self.shared_state = SharedState.get_instance()
            
            # Get ports from shared state
            xpub_port, xsub_port = self.shared_state.get("Orcustrator.XPub"), self.shared_state.get("Orcustrator.XSub")

            # Check if control is enabled
            self._control_enabled = self.shared_state.get("Orcustrator.ExternalController")
            # No need to assign external_control_port here anymore
            # if self._control_enabled:
            #    self.external_control_port = PortManager.get_free_port()

            logger.debug(f"[{self.topic}] Control mode from shared state: {self._control_enabled}")
            
            # If control is enabled, start paused and wait for commands
            # Otherwise, start in active mode
            self.paused = self._control_enabled
            
            if xpub_port is None or xsub_port is None:
                raise RuntimeError("Proxy ports not found in shared state. Did you start the proxy?")
                
            self.pub_socket.connect(f"tcp://127.0.0.1:{xsub_port}")
            
            if self._control_enabled:
                logger.debug(f"[{self.topic}] Publisher created with external control enabled")
            else:
                logger.debug(f"[{self.topic}] Publisher created with external control disabled)")
                
        except Exception as e:
            logger.error(f"[{self.topic}] Failed to initialize publisher: {e}")
            raise RuntimeError(f"Failed to get XSUB port from shared state. Did you start the proxy? Error: {e}")

    async def start_command_listener(self):
        """Start listening for commands on a separate socket if control is enabled."""
        # Skip if control is not enabled or listener is already running
        if not self._control_enabled:
            return
            
        if self.command_socket or self._command_task:
            return
            
        command_port = self.shared_state.get("Orcustrator.CommandPort")
        if not command_port:
            logger.error(f"[{self.topic}] External control enabled, but CommandPort not found in SharedState. Cannot start listener.")
            return

        self.command_socket = self.ctx.socket(zmq.SUB)
        # Connect to the centrally defined port
        connect_address = f"tcp://127.0.0.1:{command_port}"
        self.command_socket.connect(connect_address)
        self.command_socket.setsockopt_string(zmq.SUBSCRIBE, "COMMAND") # Subscribe to the command topic
        logger.success(f"[{self.topic}] Listening for commands on {connect_address}")
        
        self._command_task = asyncio.create_task(self._command_loop())

    async def _command_loop(self):
        """Background task that handles incoming commands."""
        if not self._control_enabled:
            return
            
        logger.debug(f"[{self.topic}] Command listener started - current state: {'STOPPED' if self.stopped else 'PAUSED' if self.paused else 'ACTIVE'}")
        
        # Add a counter to track if we're receiving any messages
        message_count = 0
        last_log_time = time.time()
        
        while True:
            # Check if socket is still valid before attempting to receive
            if not self.command_socket:
                 logger.warning(f"[{self.topic}] Command socket closed, exiting command loop.")
                 break
            try:
                # Log periodically if we're not receiving any messages
                current_time = time.time()
                if current_time - last_log_time > 5.0:  # Log every 5 seconds
                    logger.debug(f"[{self.topic}] Command listener still active, received {message_count} messages so far")
                    last_log_time = current_time
                
                # Use a timeout to avoid blocking forever
                try:
                    parts = await asyncio.wait_for(
                        self.command_socket.recv_multipart(),
                        timeout=1.0  # 1 second timeout
                    )
                    message_count += 1
                    
                    if len(parts) < 2:
                        logger.error(f"[{self.topic}] Received incomplete command message with {len(parts)} parts")
                        continue
                        
                    topic = parts[0].decode('utf-8')
                    payload = parts[1].decode('utf-8')
                    
                    try:
                        cmd_obj = json.loads(payload)
                        
                        # Process command directly without device targeting
                        cmd = cmd_obj.get("command", "").upper()
                        logger.warning(f"[{self.topic}] Processing command: {cmd}")
                        
                        if cmd == "START":
                            if self.stopped:
                                logger.debug(f"[{self.topic}] Cannot START - publisher is STOPPED")
                            elif not self.paused:  # Already started
                                logger.debug(f"[{self.topic}] Already ACTIVE")
                            else:
                                self.paused = False
                                self._first_publish = True  # Reset first publish flag
                                self.send_control_message("STARTED")
                                logger.debug(f"[{self.topic}] Publisher STARTED")
                            
                        elif cmd == "PAUSE":
                            if self.stopped:
                                logger.debug(f"[{self.topic}] Cannot PAUSE - publisher is STOPPED")
                            elif self.paused:
                                logger.debug(f"[{self.topic}] Already PAUSED")
                            else:
                                self.paused = True
                                self.send_control_message("PAUSED")
                                logger.debug(f"[{self.topic}] Publisher PAUSED")
                            
                        elif cmd == "RESUME":
                            if self.stopped:
                                logger.debug(f"[{self.topic}] Cannot RESUME - publisher is STOPPED")
                            elif not self.paused:
                                logger.debug(f"[{self.topic}] Already ACTIVE")
                            else:
                                self.paused = False
                                self.send_control_message("RESUMED")
                                logger.debug(f"[{self.topic}] Publisher RESUMED")
                            
                        elif cmd == "STOP":
                            if self.stopped:
                                logger.debug(f"[{self.topic}] Already STOPPED")
                            else:
                                self.send_control_message("END")
                                self.close()
                                logger.debug(f"[{self.topic}] Publisher STOPPED")
                                break # Exit loop immediately after processing STOP
                        else:
                            logger.error(f"[{self.topic}] Unknown command: {cmd}")
                    except json.JSONDecodeError:
                        logger.error(f"[{self.topic}] Invalid command JSON: {payload}")
                        continue
                    
                except asyncio.TimeoutError:
                    # No message received within timeout, just continue the loop
                    continue
            except asyncio.CancelledError:
                logger.debug(f"[{self.topic}] Command listener stopping")
                break
            except Exception as e:
                # Check if the socket became None *during* the recv attempt or other processing
                if not self.command_socket:
                    logger.warning(f"[{self.topic}] Command socket closed during loop execution, exiting.")
                else:
                    logger.error(f"[{self.topic}] Command error: {e}", exc_info=True)
                break # Exit loop on other exceptions too, to be safe

    def send_control_message(self, message: str):
        """Send a control message on the device topic."""
        try:
            self.pub_socket.send_multipart([
                self.topic.encode('utf-8'),
                f"control:{message}".encode('utf-8')
            ])
            logger.debug(f"[{self.topic}] Sent control: {message}")
        except Exception as e:
            logger.error(f"[{self.topic}] Control message error: {e}")

    def publish(self, data: np.ndarray):
        """
        Publish data as JSON for improved compatibility and ease of use.
        
        Args:
            data: NumPy array with shape (8, 25) - 8 channels, 25 samples
        """
        if self.stopped:
            return
            
        if self.paused:
            return
            
        try:
            # Send first publish notification if needed
            if self._first_publish:
                # self.send_control_message("START") # Control message might be less useful now
                self._first_publish = False
                self._first_publish_timestamp = time.time_ns() # Record the first timestamp
                logger.success(f"[{self.topic}] publishing ...")
            
            # Generate sequence number
            seq_num = int(self._msg_counter)
            self._msg_counter += 1
            
            
            # Create JSON message with minimal structure
            json_message = {
                "seq": seq_num,
                "starting_timestamp": self._first_publish_timestamp, # Use the first timestamp
                "data": data.tolist() # Convert np array to list
            }
            # Convert to JSON string
            message = json.dumps(json_message)
            # logger.success(f"[{self.topic}] Publishing message: {message}")
            # Send as a single message with topic prefix
            self.pub_socket.send_multipart([
                self.topic.encode('utf-8'),
                message.encode('utf-8')
            ])
            logger.error(json_message)
            if self._msg_counter % 1000 == 0:  # Log less frequently
                logger.debug(f"[{self.topic}] Published message #{self._msg_counter} with shape {data.shape}")
            
        except Exception as e:
            logger.error(f"[{self.topic}] Publish error: {e}")
            raise

    def close(self):
        """Clean shutdown of publisher."""
        if not self.stopped:
            self.send_control_message("END")
            self.stopped = True
            logger.debug(f"[{self.topic}] Publisher entering STOPPED state")
            
        if self._command_task:
            self._command_task.cancel()
            
        if self.command_socket:
            self.command_socket.close()
            self.command_socket = None
            
        self.pub_socket.close()
        logger.debug(f"[{self.topic}] Publisher fully closed and cleaned up")