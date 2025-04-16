from typing import Dict, Optional, List
import asyncio
from .device import Device
from ..utils.logger import logger
from ..utils.shared_state import SharedState
import time
import math

class DeviceManager:
    """
    A manager that creates and stores references to multiple devices.
    """
    def __init__(self):
        self.devices: Dict[str, 'Device'] = {} # Dictionary to store devices instances by topic
        self.is_streaming = False
        self.shared_state = SharedState.get_instance()
        self._stream_tasks = []

    async def set_devices(self) -> List['Device']:
        """
        Set up all devices configured in shared state.
        Returns a list of successfully created devices.
        """
        devices = []
        device_configs = self.shared_state.get("Devices", {})
        for topic, _ in device_configs.items():
            # Create the device
            device = Device(topic=topic)
            # Set the device_manager reference so the device can start the metadata responder when needed
            device.device_manager = self
            await device.setup()
            
            # Save the device in the registry
            self.devices[topic] = device
            devices.append(device)

    async def connect(self):   
        """Connect a list of devices concurrently."""
        await asyncio.gather(*(d.connect() for d in self.devices.values()))

    async def start_streaming(self):
        """
        Start streaming for all devices and wait indefinitely.
        This method will block until interrupted.
        """
        if not self.devices:
            logger.warning("No devices available to start streaming")
            return

        try:
            # Start streaming for all devices
            self._stream_tasks = []
            for device in self.devices.values():
                task = asyncio.create_task(device.start_stream())
                self._stream_tasks.append(task)
            
            self.is_streaming = True
            logger.info(f"Started streaming for {len(self._stream_tasks)} devices")
            
            # Wait for all stream tasks to complete
            if self._stream_tasks:
                # Save in the SharedState the beginning of the stream in nanoseconds as "starting_timestamp"
                start_time_ns = time.time_ns()
                self.shared_state.set("StartingTimestamp", start_time_ns)

                # --- Check for finite duration and start logger task ---
                log_task = None
                tasks_to_wait_on = list(self._stream_tasks) # Copy the list
                stream_duration = self.shared_state.get("StreamDuration")

                if stream_duration is not None and stream_duration != float('inf'):
                    try:
                        total_duration_float = float(stream_duration)
                        if total_duration_float > 0:
                            log_task = asyncio.create_task(
                                self._log_remaining_time(total_duration_float, start_time_ns),
                                name="RemainingTimeLogger"
                            )
                            tasks_to_wait_on.append(log_task)
                    except (ValueError, TypeError) as e:
                        logger.warning(f"Could not parse StreamDuration '{stream_duration}' as float: {e}. Cannot start remaining time logger.")
                # --------------------------------------------------------

                await asyncio.gather(*self._stream_tasks, return_exceptions=True)

                await asyncio.gather(*tasks_to_wait_on, return_exceptions=True)

        except asyncio.CancelledError:
            logger.info("Streaming cancelled")
            raise
        finally:
            self.is_streaming = False
            # Cancel any remaining stream tasks
            tasks_to_cancel = self._stream_tasks + ([log_task] if log_task else [])
            for task in tasks_to_cancel:
                if not task.done():
                    task.cancel()
            
            # Wait for tasks to complete
            if tasks_to_cancel:
                await asyncio.gather(*tasks_to_cancel, return_exceptions=True)
            self._stream_tasks = []

    async def _log_remaining_time(self, total_duration: float, start_time_ns: int):
        """Periodically logs the remaining stream time."""
        start_time = start_time_ns / 1e9 # Convert ns to seconds
        logger.debug(f"Starting periodic remaining time log. Total duration: {total_duration}s")
        try:
            while True:
                await asyncio.sleep(10) # Wait for 1 minute

                current_time = time.time()
                elapsed_time = current_time - start_time
                remaining_time = total_duration - elapsed_time

                if remaining_time <= 0:
                    logger.debug("Remaining time logger exiting: duration elapsed.")
                    break

                if remaining_time <= 60:
                    logger.success(f"Remains: {remaining_time:.0f} seconds")
                else:
                    remaining_minutes = math.ceil(remaining_time / 60)
                    logger.success(f"Remains: {remaining_minutes} min")

        except asyncio.CancelledError:
            logger.debug("Remaining time logger cancelled.")
        except Exception as e:
            logger.error(f"Error in remaining time logger: {e}", exc_info=True)

    async def disconnect(self):
        """Disconnect a list of devices concurrently."""
        await asyncio.gather(*(d.disconnect() for d in self.devices.values()))
        
    async def shutdown(self):
        """
        Shutdown the device manager.
        """
        # Stop streaming if active
        if self.is_streaming:
            for task in self._stream_tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*self._stream_tasks, return_exceptions=True)
            self._stream_tasks = []
            
        # Disconnect any remaining devices
        if self.devices:
            await self.disconnect()
            logger.debug(f"Disconnected {len(self.devices)} devices during shutdown")