import zmq
import time
import numpy as np
import asyncio
import json
import inspect
from typing import Optional, Callable, Dict, Any, Tuple, Union
from ..utils.logger import logger

class DataSubscriber:
    """
    Generic subscriber for binary data from the CognitiveSDK ZeroMQ proxy.
    
    This subscriber handles:
    1. Connection to the ZeroMQ proxy
    2. Receiving binary messages
    3. Parsing binary data with timestamps and shapes
    4. Providing callbacks for data processing
    
    Usage:
        # Create and configure subscriber
        sub = DataSubscriber(topic_filter="museA.EEG")
        
        # Define a callback
        def on_data(timestamp, data, metadata):
            print(f"Received data with shape {data.shape}, timestamp: {timestamp}")
        
        # Set the callback
        sub.set_data_callback(on_data)
        
        # Start receiving (blocking)
        sub.receive(timeout=30)
        
        # Or in an async context
        await sub.receive_async(timeout=30)
    """
    
    def __init__(self, 
                 topic_filter: str = "", 
                 xpub_port: Optional[int] = None):
        """
        Initialize the subscriber.
        
        Args:
            topic_filter: ZeroMQ topic filter string (empty receives all messages)
            xpub_port: The XPUB port of the proxy to connect to.
        """
        self.topic_filter = topic_filter
        self.xpub_port = xpub_port
        self._ctx = None
        self._socket = None
        self._running = False
        self._data_callback = None
        self._error_callback = None
        self._message_counter = 0
    
    async def connect_async(self) -> None:
        """Connect to the ZeroMQ proxy using the provided XPUB port."""
        if self._socket is not None:
            logger.debug("Subscriber already connected")
            return
        
        try:
            if not self.xpub_port:
                raise ValueError("XPUB port not provided during initialization.")
            
            logger.debug(f"Connecting to XPUB port: {self.xpub_port}")
            
            # Set up ZeroMQ context and socket
            self._ctx = zmq.Context.instance()
            self._socket = self._ctx.socket(zmq.SUB)
                   
            # Connect to the proxy
            self._socket.connect(f"tcp://localhost:{self.xpub_port}")
            
            # Subscribe to the topic filter
            self._socket.setsockopt_string(zmq.SUBSCRIBE, self.topic_filter)
            
            logger.info(f"Connected to proxy and subscribed to: '{self.topic_filter or 'all topics'}'")
            
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise
    
    def connect(self) -> None:
        """
        Deprecated synchronous connect method.
        Use connect_async() instead.
        """
        logger.warning("connect() is deprecated, use connect_async() instead")
        try:
            asyncio.get_event_loop().run_until_complete(self.connect_async())
        except RuntimeError as e:
            if "cannot be called from a running event loop" in str(e):
                raise RuntimeError("connect() cannot be called from an async context. Use connect_async() instead.") from e
            raise

    async def receive_async(self, timeout: Optional[float] = None) -> int:
        """
        Asynchronously receive and process messages.
        
        Args:
            timeout: Maximum duration to receive (None = run indefinitely)
            
        Returns:
            Number of messages processed
        """ 
        if self._socket is None:
            await self.connect_async()
            
        self._running = True
        self._message_counter = 0
        
        start_time = time.time()
        end_time = float('inf') if timeout is None else start_time + timeout
        try:
            while self._running and time.time() < end_time :
                try:
                    # Try to receive a multipart message
                    multipart_message = self._socket.recv_multipart(flags=zmq.NOBLOCK)
                    self._message_counter += 1
                    # The first part is the topic, the second part is the actual data
                    if len(multipart_message) >= 2:
                        topic = multipart_message[0].decode('utf-8')
                        message = multipart_message[1]  # Get the payload bytes
                        
                        # --- Check for Control Message --- 
                        if message.startswith(b'control:'):
                             control_msg_content = message.decode('utf-8', errors='ignore')
                             logger.info(f"Received control message on {topic}: {control_msg_content}")
                             # Optionally, handle specific control messages like 'control:END'
                             # if control_msg_content == 'control:END':
                             #     self.stop() # Example: signal loop to stop
                             continue # Skip JSON parsing for control messages
                        # --- End Control Message Check ---
                        
                        try:
                            parsed_message = self._parse_message(message)
                            if parsed_message:
                                parsed_message["topic"] = topic
                                # Call the callback if set
                                if self._data_callback is not None:
                                    # Check if the callback is an async function
                                    if inspect.iscoroutinefunction(self._data_callback):
                                        logger.warning(f"[RAW RECV] Async callback")
                                        await self._data_callback(parsed_message)
                                    else:
                                        self._data_callback(parsed_message)
                                
                        except Exception as e:
                            if self._error_callback:
                                self._error_callback(e)
                            else:
                                logger.error(f"Error processing message: {e}")
                    
                except zmq.Again:
                    # No message available, yield to other tasks
                    await asyncio.sleep(0.001)
                    
        except asyncio.CancelledError:
            logger.info("Receiving cancelled")
            raise
        finally:
            self._running = False
            
        return self._message_counter

    def receive(self, timeout: Optional[float] = None, poll_interval: float = 0.01) -> int:
        """
        Receive and process messages for a specified duration.
        
        Args:
            timeout: Maximum duration to receive (None = run indefinitely)
            poll_interval: Sleep time between polls when no message is available
            
        Returns:
            Number of messages processed
        """
        try:
            return asyncio.get_event_loop().run_until_complete(self.receive_async(timeout))
        except RuntimeError as e:
            if "cannot be called from a running event loop" in str(e):
                raise RuntimeError("receive() cannot be called from an async context. Use receive_async() instead.") from e
            raise

    def set_data_callback(self, callback: Callable[[float, np.ndarray, Dict[str, Any]], None]) -> None:
        """
        Set the callback function for received data.
        
        The callback receives:
            - timestamp (float): The timestamp from the message
            - data (np.ndarray): The parsed data array
            - metadata (Dict): Additional information like shape, count, delay, etc.
        """
        self._data_callback = callback
    
    def set_error_callback(self, callback: Callable[[Exception], None]) -> None:
        """Set the callback for errors during processing."""
        self._error_callback = callback
    
    def _parse_message(self, message: bytes) -> Optional[Dict[str, Any]]:
        """
        Parse a JSON message bytes into a dictionary.
        
        Format from publisher:
        - JSON object with "seq", "starting_timestamp", and "data" keys.
        
        Returns:
            The parsed dictionary, or None if parsing fails.
        """
        try:
            # Decode JSON message
            json_data = json.loads(message.decode('utf-8'))
            
            # Basic validation (optional, could be done by consumer)
            if not all(k in json_data for k in ["seq", "starting_timestamp", "data"]):
                logger.warning(f"Parsed JSON missing expected keys: {json_data.keys()}")
                # Depending on requirements, might return None or the partial dict
                # return None 
            
            return json_data # Return the raw dictionary
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON message: {e}")
            return None
        except Exception as e: # Catch other potential errors during validation/parsing
            logger.error(f"Unexpected error parsing message: {e}")
            raise
    
    def stop(self) -> None:
        """Stop the receiving loop."""
        self._running = False
    
    def close(self) -> None:
        """Close the ZeroMQ socket and clean up resources."""
        if self._socket:
            self._socket.close()
            
        # The context will be terminated when the process exits
        logger.debug("Subscriber closed")