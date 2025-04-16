# devices/middlewares/brainflow.py

import asyncio
import threading
import numpy as np
from typing import Optional
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds, BrainFlowPresets, BrainFlowError
from ...utils.logger import logger
from ...utils.shared_state import SharedState
import time

# Timeout for inactivity in the read loop (in seconds)
READ_LOOP_INACTIVITY_TIMEOUT = 10.0

class BrainflowInterface:
    def __init__(self, device):
        self.device = device
        self.params = BrainFlowInputParams()
        self.board_shim: Optional[BoardShim] = None
        self._running = False
        self.read_task: Optional[asyncio.Task] = None
        self._initialized = False
        self._brainflow_lock = threading.Lock()
        self.shared_state = SharedState.get_instance()
        # Setup board ID
        self.params.serial_port = self.device.device_serial_number
        self.board_id = self._resolve_board_id(self.device.device_metadata.get("DeviceBoardName", ""))        
        self._preset_map = {
            "DEFAULT": BrainFlowPresets.DEFAULT_PRESET.value,
            "ANCILLARY": BrainFlowPresets.ANCILLARY_PRESET.value,
            "AUXILIARY": BrainFlowPresets.AUXILIARY_PRESET.value
        }
        BoardShim.disable_board_logger()

        #log metadata 
    def _resolve_board_id(self, board_name):
        """Get the BoardIds enum value for the given board identifier."""
        if isinstance(board_name, int):
            return board_name
        
        if not isinstance(board_name, str):
            raise TypeError(f"Board identifier must be int or str, got {type(board_name).__name__}")
            
        board_name = board_name.strip().upper()
        if board_name.lower() == "synthetic":
            return BoardIds.SYNTHETIC_BOARD.value
        
        try:
            return getattr(BoardIds, board_name).value
        except AttributeError:
            raise ValueError(f"Board name '{board_name}' does not match any known BoardIds.")

    async def prepare(self):
        if self._initialized:
            logger.warning(f"Board {self.device.device_name} already prepared.")
            return
        max_retries = 3
        delay = 1.0
        for attempt in range(max_retries):
            with self._brainflow_lock:
                try:
                    self.board_shim = BoardShim(self.board_id, self.params)
                    await asyncio.to_thread(self.board_shim.prepare_session)
                    self._initialized = True
                    logger.success(f"Connected to {self.device.device_name} [{self.params.serial_port}]")
                    return
                except BrainFlowError as e:
                    logger.error(f"Failed to connect to {self.device.device_name} [{self.params.serial_port}] (attempt {attempt+1}): {e}")
                    self.board_shim = None
                    if attempt < max_retries - 1:
                        await asyncio.sleep(delay)
                        delay *= 1.5
                    else:
                        raise BrainFlowError(f"Could not connect to {self.device.device_name} after {max_retries} attempts.")

    async def start_stream(self):
        if not self._initialized:
            await self.prepare()

        with self._brainflow_lock:
            # Create a streamer parameter to save data to CSV file
            # csv_path = f"file://{self.device.device_name}_{self.params.serial_port}_recording.csv:w"
            # await asyncio.to_thread(self.board_shim.start_stream, streamer_params=csv_path)
            await asyncio.to_thread(self.board_shim.start_stream)
            # logger.info(f"Saving BrainFlow data to {csv_path.replace('file://', '').replace(':w', '')}")
            self._running = True

        self.read_task = asyncio.create_task(self._read_loop())
        logger.success(f"Started Brainflow streaming for {self.device.device_name}_{self.params.serial_port}")

    async def stop_stream(self):
        """Stop the BrainFlow stream, attempting to fetch and publish any remaining data first."""
        if not self._running:
            logger.info(f"Stream for {self.device.device_name}_{self.params.serial_port} already stopped.")
            return
        logger.info(f"Initiating stream stop for {self.device.device_name}_{self.params.serial_port}...")

        self._running = False # Signal the read loop to stop
        if self.read_task:
            self.read_task.cancel()
            try:
                await self.read_task
            except asyncio.CancelledError:
                logger.info(f"Read loop for {self.device.device_name}_{self.params.serial_port} successfully cancelled.")

        # --- Attempt to fetch and publish remaining data --- 
        logger.info(f"Attempting to fetch remaining data for {self.device.device_name}_{self.params.serial_port} before stopping stream...")
        if self.board_shim:
            try:
                with self._brainflow_lock:
                    for subdevice in self.device.subdevices:
                        try:
                            preset = subdevice.config.get("Preset", "DEFAULT")
                            preset_val = self._preset_map.get(preset, BrainFlowPresets.DEFAULT_PRESET.value)
                            channels_index = subdevice.channel_indices

                            remaining_count = await asyncio.to_thread(self.board_shim.get_board_data_count, preset_val)
                            if remaining_count > 0:
                                logger.info(f"Found {remaining_count} remaining samples for {subdevice.name}. Fetching and publishing...")
                                final_data = await asyncio.to_thread(self.board_shim.get_board_data, remaining_count, preset_val)
                                if final_data is not None and final_data.size > 0:
                                    sliced_final_data = final_data[channels_index, :]
                                    # Use a non-async call here as we are inside a to_thread lock implicitly
                                    try:
                                         subdevice.on_data(sliced_final_data)
                                         logger.debug(f"Published {sliced_final_data.shape[1]} final samples for {subdevice.name}.")
                                    except Exception as pub_e:
                                         logger.error(f"Error publishing final samples for {subdevice.name}: {pub_e}")
                                else:
                                     logger.warning(f"get_board_data returned None or empty for {subdevice.name} despite count {remaining_count}")
                        except BrainFlowError as bf_e:
                             logger.error(f"BrainFlow error fetching final data for {subdevice.name}: {bf_e}")
                        except Exception as e:
                             logger.error(f"Unexpected error fetching final data for {subdevice.name}: {e}")
            except Exception as final_fetch_e:
                 logger.error(f"Error during final data fetch block: {final_fetch_e}")
        else:
             logger.warning(f"Board shim not available, cannot fetch remaining data for {self.device.device_name}_{self.params.serial_port}.")
        # --- End final data fetch --- 

        if self.board_shim:
            with self._brainflow_lock:
                logger.info(f"Stopping BrainFlow stream for {self.device.device_name}_{self.params.serial_port}...")
                await asyncio.to_thread(self.board_shim.stop_stream)
                logger.info(f"BrainFlow stream stopped for {self.device.device_name}_{self.params.serial_port}.")

    async def release_session(self):
         """Release the BrainFlow session."""
         if self.board_shim:
             with self._brainflow_lock:
                 logger.info(f"Releasing BrainFlow session for {self.device.device_name}_{self.params.serial_port}...")
                 await asyncio.to_thread(self.board_shim.release_session)
                 logger.info(f"Brainflow session released for {self.device.device_name}_{self.params.serial_port}.")
             self.board_shim = None
             self._initialized = False
         else:
              logger.info(f"No active BrainFlow session to release for {self.device.device_name}_{self.params.serial_port}.")

    async def _read_loop(self):
        """Read data from board and publish to subdevices using a rate-based approach."""
        last_data_received_time = time.monotonic()
        try: # Outer try for loop errors/cancellation
            while self._running:
                data = None # Reset data for each outer loop iteration
                data_fetched_this_iteration = False # Flag to check if any subdevice got data

                # Check for inactivity timeout before processing subdevices
                current_time = time.monotonic()
                if current_time - last_data_received_time > READ_LOOP_INACTIVITY_TIMEOUT:
                     logger.warning(f"No data received for {READ_LOOP_INACTIVITY_TIMEOUT:.1f} seconds. Stopping read loop for {self.device.device_name}.")
                     self._running = False # Signal loop termination
                     break # Exit the while loop

                for subdevice in self.device.subdevices:
                    # Note: 'data' might retain value from previous subdevice iteration if fetch fails here
                    try: # Inner try specifically for BrainFlow operations within the lock
                        with self._brainflow_lock:
                            # Ensure epoch_length and sampling_frequency are valid
                            sampling_frequency = subdevice.sampling_frequency
                            preset = subdevice.config.get("Preset", "DEFAULT") # Use DEFAULT preset as a fallback
                            preset_val = self._preset_map.get(preset, BrainFlowPresets.DEFAULT_PRESET.value)
                            channels_index = subdevice.channel_indices

                            if int(self.device.epoch_length) <= 0 or int(sampling_frequency) <= 0:
                                logger.warning(f"Invalid epoch length ({self.device.epoch_length}) or sampling rate ({sampling_frequency}). Skipping read.")
                                await asyncio.sleep(0.1)
                                continue # Skip to next subdevice

                            data_count = self.board_shim.get_board_data_count(preset_val)
                            # Use >= to avoid missing data if exactly epoch_length_samples are available
                            if data_count >= int(self.device.epoch_length):
                                # Fetch data based on the current subdevice's preset
                                fetched_preset_data = await asyncio.to_thread(self.board_shim.get_board_data, int(self.device.epoch_length), preset_val)
                                # Slice the fetched data using the current subdevice's channel indices
                                sliced_data = fetched_preset_data[channels_index, :]
                               
                                # --- Dispatch data immediately after successful fetch/slice --- 
                                try:
                                    subdevice.on_data(sliced_data)
                                    last_data_received_time = time.monotonic() # Update time on successful dispatch
                                    data_fetched_this_iteration = True
                                except Exception as e:
                                    logger.error(f"Error sending data to subdevice {subdevice.name}: {e}")
                                
                                # Set data to None *after* potential dispatch to prevent reuse in outer check
                                data = None 
                            else: # Not enough data for this preset/subdevice yet
                               data = None # Explicitly set data to None if not enough samples

                    except BrainFlowError as e:
                        logger.error(f"BrainFlow error during data read for {subdevice.name}: {e}")
                        data = None # Ensure data is None on error
                        await asyncio.sleep(0.1)
                        # Continue to next subdevice, don't skip outer sleep
                    except Exception as e:
                        logger.error(f"Unexpected error during locked BrainFlow operation for {subdevice.name}: {e}")
                        data = None # Ensure data is None on error
                        await asyncio.sleep(0.1)
                        # Continue to next subdevice, don't skip outer sleep

                # Small sleep outside the lock to yield control and prevent busy-waiting
                await asyncio.sleep(0.001)

        except asyncio.CancelledError:
            logger.info("Read loop cancelled")
        except Exception as e: # Catch errors in the outer loop setup/logic
            logger.error(f"Fatal error in read loop: {e}", exc_info=True)
            raise
