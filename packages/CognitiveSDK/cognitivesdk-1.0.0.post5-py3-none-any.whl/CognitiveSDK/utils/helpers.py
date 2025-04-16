import asyncio
import importlib
import re
from typing import Dict, Any, Optional, Coroutine, Union, Tuple, List
import copy
import os
import json
import numpy as np
import pandas as pd

# Use relative import based on file location within utils
from .logger import logger 

def camel_to_snake(word: str) -> str:
    """Convert CamelCase string to snake_case."""
    # Add _ between acronym and next word (e.g., HTTPRequest -> HTTP_Request)
    word = re.sub(r"([A-Z]+)([A-Z][a-z])", r'\1_\2', word)
    # Add _ between lowercase/digit and uppercase (e.g., SimpleCase -> Simple_Case)
    word = re.sub(r"([a-z\d])([A-Z])", r'\1_\2', word)
    # Optional: handle dashes if needed, uncomment below
    # word = word.replace("-", "_")
    return word.lower()

async def start_single_external_subscriber(
    config_item: Union[str, Dict[str, Any]], 
    metadata_port: int
) -> Optional[Tuple[str, Dict[str, Any]]]:
    """
    Loads, instantiates, and starts a single external subscriber based on config.

    Args:
        config_item: Configuration (either class name string or dictionary).
        metadata_port: The port for the metadata service.

    Returns:
        A tuple containing (subscriber_key, {"instance": obj, "task": task}) or None on failure.
    """
    class_name = None
    module_path = None
    init_args = {}

    # Determine module_path, class_name, and init_args based on config_item type
    if isinstance(config_item, str):
        class_name = config_item
        module_name_part = camel_to_snake(class_name)
        # Construct the path assuming subscribers are in a top-level 'subscriber' directory.
        module_path = f"subscriber.{module_name_part}"
        logger.debug(f"Inferred module path '{module_path}' for class '{class_name}'")
    elif isinstance(config_item, dict):
        module_path = config_item.get("module_path")
        class_name = config_item.get("class_name")
        init_args = config_item.get("init_args", {})
    else:
        logger.error(f"Invalid configuration type in ExternalSubscriberList: {config_item}")
        return None
    
    if not module_path or not class_name:
        logger.error(f"Could not determine module_path or class_name for config: {config_item}")
        return None

    subscriber_key = f"{module_path}.{class_name}"

    try:
        logger.debug(f"Loading external subscriber: {subscriber_key}")
        module = importlib.import_module(module_path)
        SubscriberClass = getattr(module, class_name)
        
        # Add metadata_port (always add this)
        init_args["metadata_port"] = metadata_port
        
        instance = SubscriberClass(**init_args)
        logger.info(f"Instantiated: {subscriber_key} with args {init_args}")

        # Ensure instance.start exists and is callable
        if not (hasattr(instance, 'start') and callable(instance.start)):
             logger.error(f"Subscriber class {subscriber_key} does not have a callable 'start' method.")
             return None
        
        task = asyncio.create_task(instance.start())
        logger.info(f"Started task for: {subscriber_key}")
        
        return subscriber_key, {"instance": instance, "task": task}
        
    except ModuleNotFoundError:
        logger.error(f"Module not found: {module_path}")
    except AttributeError:
        # More specific error if start() is missing vs class not found
        logger.error(f"Class '{class_name}' not found in '{module_path}' or instance missing 'start' method") 
    except TypeError as e:
         logger.error(f"Error instantiating '{subscriber_key}' with args {init_args}: {e}")
    except Exception as e:
        logger.error(f"Error starting {subscriber_key}: {e}", exc_info=True)
        
    return None

async def stop_single_external_subscriber(
    key: str, 
    instance: Any, 
    task: asyncio.Task
) -> Optional[asyncio.Task]: # Return task if cancellation needed
    """Stops and cleans up a single external subscriber instance and task.
    
    Returns the task if it needed cancellation, otherwise None.
    """
    logger.debug(f"Stopping: {key}")
    try:
        if hasattr(instance, 'stop') and callable(instance.stop):
            stop_method = instance.stop
            if asyncio.iscoroutinefunction(stop_method):
                await stop_method()
            else:
                # If stop is synchronous, call it directly. 
                # Consider asyncio.to_thread if it might block significantly.
                stop_method()
            logger.debug(f"Called stop() on {key}")
    except Exception as e:
        logger.error(f"Error calling stop() on {key}: {e}")

    # Cancel the task if it's still running
    if task and not task.done():
         logger.debug(f"Cancelling task for {key}")
         task.cancel()
         return task # Return task to be awaited by caller
    return None 

def extract_topics_with_rates(devices_state: Dict[str, Any]) -> Dict[str, Optional[int]]:
    """
    Extracts a dictionary of {topic_name: sampling_rate} from the devices state structure.

    Args:
        devices_state: The 'Devices' dictionary from SharedState.

    Returns:
        A dictionary mapping full topic names to their sampling rates (or None).
    """
    extracted_topics = {}
    logger.debug(f"Extracting topics from {len(devices_state)} devices provided...")
    for device_name, device_info in devices_state.items():
        if isinstance(device_info, dict):
            selected_middleware = device_info.get("SelectedMiddleware")
            if selected_middleware:
                middlewares = device_info.get("AvailableMiddlewares", {})
                middleware_info = middlewares.get(selected_middleware, {})
                subdevices = middleware_info.get("SubDevices", {})
                if not subdevices:
                    logger.debug(f"No SubDevices found for {device_name} under middleware {selected_middleware}.")
            else:
                logger.debug(f"No SelectedMiddleware found for device '{device_name}'.")
                subdevices = {}
                
            for sub_name, sub_info in subdevices.items():
                if isinstance(sub_info, dict): # Ensure sub_info is a dict before accessing keys
                    full_topic_name = f"{device_name}.{sub_name}"
                    # Use the correct key from the state structure
                    sampling_rate = sub_info.get("SamplingFrequency") 
                    extracted_topics[full_topic_name] = sampling_rate
                else:
                    logger.warning(f"Expected dict for subdevice '{sub_name}' under device '{device_name}', but got {type(sub_info)}. Skipping.")
        else:
            logger.warning(f"Expected dict for device '{device_name}', but got {type(device_info)}. Skipping.")
                
    return extracted_topics 

# New helper functions added below

def get_subdevice_topics(devices_state: Dict[str, Any]) -> List[str]:
    """
    Extracts a list of full subdevice topic names (e.g., ["DeviceName.SubDeviceName"]).

    Args:
        devices_state: The 'Devices' dictionary from SharedState.

    Returns:
        A list of strings representing the full topic names.
    """
    subdevice_topics = []
    logger.debug(f"Extracting subdevice topics from {len(devices_state)} devices provided...")
    for device_name, device_info in devices_state.items():
        if isinstance(device_info, dict):
            selected_middleware = device_info.get("SelectedMiddleware")
            if selected_middleware:
                middlewares = device_info.get("AvailableMiddlewares", {})
                middleware_info = middlewares.get(selected_middleware, {})
                subdevices = middleware_info.get("SubDevices", {})
                if not subdevices:
                    logger.debug(f"No SubDevices found for {device_name} under middleware {selected_middleware}.")
                else:
                    for sub_name in subdevices.keys():
                         full_topic_name = f"{device_name}.{sub_name}"
                         subdevice_topics.append(full_topic_name)
            else:
                logger.debug(f"No SelectedMiddleware found for device '{device_name}'. Cannot extract subdevice topics.")
        else:
            logger.warning(f"Expected dict for device '{device_name}', but got {type(device_info)}. Skipping topic extraction.")
                
    return subdevice_topics

def get_device_names(devices_state: Dict[str, Any]) -> List[str]:
    """
    Extracts a list of device names from the devices state structure.

    Args:
        devices_state: The 'Devices' dictionary from SharedState.

    Returns:
        A list of strings representing the device names (keys of the dictionary).
    """
    if not isinstance(devices_state, dict):
        logger.error(f"Expected devices_state to be a dict, but got {type(devices_state)}")
        return []
    return list(devices_state.keys())

def get_devices(devices_state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Processes the devices state to only include selected middleware data under a 'Middleware' key.

    Args:
        devices_state: The 'Devices' dictionary from SharedState.

    Returns:
        A dictionary representing the devices with middleware data restructured.
    """
    processed_devices = {}
    logger.debug(f"Processing device structure for {len(devices_state)} devices...")
    if not isinstance(devices_state, dict):
        logger.error(f"Expected devices_state to be a dict, but got {type(devices_state)}")
        return {}
        
    for device_name, device_info in devices_state.items():
        if not isinstance(device_info, dict):
            logger.warning(f"Expected dict for device '{device_name}', but got {type(device_info)}. Skipping processing.")
            continue

        # Deep copy to avoid modifying the original state accidentally elsewhere
        new_device_info = copy.deepcopy(device_info)
        
        selected_middleware = new_device_info.pop("SelectedMiddleware", None)
        available_middlewares = new_device_info.pop("AvailableMiddlewares", {})

        if selected_middleware and selected_middleware in available_middlewares:
            # Add the selected middleware's data under the 'Middleware' key
            new_device_info["Middleware"] = available_middlewares[selected_middleware]
            logger.debug(f"Processed middleware for device '{device_name}'. Selected: {selected_middleware}")
        else:
            # Handle cases where middleware isn't selected or found
            new_device_info["Middleware"] = {} # Assign empty dict if not found/selected
            if selected_middleware:
                 logger.warning(f"SelectedMiddleware '{selected_middleware}' not found in AvailableMiddlewares for device '{device_name}'.")
            else:
                 logger.debug(f"No SelectedMiddleware for device '{device_name}'.")

        processed_devices[device_name] = new_device_info
                
    return processed_devices

def get_subdevices(devices_state: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Extracts a dictionary mapping device names to their selected subdevice configurations.

    Args:
        devices_state: The 'Devices' dictionary from SharedState.

    Returns:
        A dictionary where keys are device names and values are the 'SubDevices' 
        dictionaries from the selected middleware.
    """
    all_subdevices = {}
    logger.debug(f"Extracting subdevices for {len(devices_state)} devices...")
    if not isinstance(devices_state, dict):
        logger.error(f"Expected devices_state to be a dict, but got {type(devices_state)}")
        return {}
        
    for device_name, device_info in devices_state.items():
        if isinstance(device_info, dict):
            selected_middleware = device_info.get("SelectedMiddleware")
            if selected_middleware:
                middlewares = device_info.get("AvailableMiddlewares", {})
                middleware_info = middlewares.get(selected_middleware, {})
                subdevices = middleware_info.get("SubDevices", {}) 
                if subdevices:
                    # Deep copy might be safer if the subdevice dicts could be modified
                    all_subdevices[device_name] = copy.deepcopy(subdevices) 
                    logger.debug(f"Extracted {len(subdevices)} subdevices for '{device_name}' using middleware '{selected_middleware}'.")
                else:
                    logger.debug(f"No SubDevices found for {device_name} under middleware {selected_middleware}.")
                    all_subdevices[device_name] = {} # Add empty dict if no subdevices
            else:
                logger.debug(f"No SelectedMiddleware found for device '{device_name}'. Cannot extract subdevices.")
                all_subdevices[device_name] = {} # Add empty dict if no middleware selected
        else:
            logger.warning(f"Expected dict for device '{device_name}', but got {type(device_info)}. Skipping subdevice extraction.")
            
    return all_subdevices

def json_to_numpy(json_path: str) -> Optional[np.ndarray]:
    """Loads CognitiveSDK cached JSON data and returns it as a NumPy array.

    The JSON file is expected to be a list of packet dictionaries,
    where each packet has a 'data' key containing a list of lists
    representing channels x samples.

    Args:
        json_path: Path to the input JSON file (e.g., merged_data.json).

    Returns:
        A NumPy array (channels x total_samples) or None if loading/processing fails.
    """
    logger.debug(f"Attempting to load JSON and convert to NumPy: {json_path}")
    if not os.path.exists(json_path):
        logger.error(f"JSON file not found: {json_path}")
        return None

    try:
        with open(json_path, 'r') as f:
            packets = json.load(f)

        if not isinstance(packets, list):
            logger.error(f"JSON content is not a list: {json_path}")
            return None
        
        if not packets:
            logger.warning(f"JSON file is empty: {json_path}")
            return None # Return None for empty list, as concatenate needs >= 1 array

        all_data_arrays = []
        for i, packet in enumerate(packets):
            if isinstance(packet, dict) and 'data' in packet:
                data_list = packet['data']
                if isinstance(data_list, list) and data_list:
                     try:
                        data_array = np.array(data_list, dtype=np.float32)
                        # Ensure it has 2 dimensions (channels, samples) and samples > 0
                        if data_array.ndim == 2 and data_array.shape[1] > 0:
                            all_data_arrays.append(data_array)
                        elif data_array.ndim != 2:
                             logger.warning(f"Packet {i} data is not 2-dimensional (Channels x Samples). Shape: {data_array.shape}. Skipping.")
                        else: # ndim == 2 but shape[1] == 0
                             logger.warning(f"Packet {i} data has 0 samples. Shape: {data_array.shape}. Skipping.")
                     except Exception as e:
                        logger.warning(f"Error converting data in packet {i} to array: {e}. Skipping packet.")
                else:
                     logger.warning(f"Packet {i} 'data' key is not a non-empty list. Skipping packet.")
            else:
                logger.warning(f"Packet {i} is not a dict or missing 'data' key. Skipping packet.")

        if not all_data_arrays:
            logger.error("No valid data packets could be processed from the JSON file.")
            return None

        # Concatenate along the samples axis (axis=1)
        concatenated_data = np.concatenate(all_data_arrays, axis=1)
        logger.success(f"Successfully loaded and concatenated data from {json_path}. Final shape: {concatenated_data.shape}")
        return concatenated_data

    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from {json_path}: {e}")
        return None
    except Exception as e:
        logger.error(f"An unexpected error occurred processing {json_path}: {e}", exc_info=True)
        return None

def json_to_csv(json_path: str, output_csv_path: Optional[str] = None, separator: str = '\t') -> bool:
    """Loads CognitiveSDK cached JSON data, converts it, and saves it as a CSV file.

    Args:
        json_path: Path to the input JSON file (e.g., merged_data.json).
        output_csv_path: Path to save the output CSV file. If None, it saves
                         the CSV next to the input JSON with a .csv extension.
        separator: The delimiter to use in the CSV file (default is tab).

    Returns:
        True if the CSV was saved successfully, False otherwise.
    """
    logger.debug(f"Starting JSON to CSV conversion for: {json_path}")
    
    # Load data using the numpy helper
    data_np = json_to_numpy(json_path)
    
    if data_np is None:
        logger.error("Failed to load data from JSON, cannot proceed with CSV conversion.")
        return False
        
    # Determine output path if not provided
    if output_csv_path is None:
        base, _ = os.path.splitext(json_path)
        output_csv_path = base + ".csv"
        logger.info(f"Output CSV path not specified, defaulting to: {output_csv_path}")
        
    try:
        num_channels = data_np.shape[0]
        num_samples = data_np.shape[1]
        logger.debug(f"Data loaded for CSV: {num_channels} channels, {num_samples} samples.")
        
        # Transpose data for CSV (Samples x Channels)
        data_transposed = data_np.T
        
        # Create default channel names
        channel_names = [f"Ch{i+1}" for i in range(num_channels)]
        
        # Create DataFrame
        df_transformed = pd.DataFrame(data_transposed, columns=channel_names)
        logger.debug(f"Created DataFrame with shape: {df_transformed.shape}")

        # Ensure output directory exists
        output_dir = os.path.dirname(output_csv_path)
        if output_dir:
             os.makedirs(output_dir, exist_ok=True)

        # Save to CSV
        df_transformed.to_csv(
            output_csv_path, 
            sep=separator, 
            header=True, 
            index=False, 
            float_format='%.6f' # Maintain precision
        )
        logger.success(f"Successfully saved transformed data to: {output_csv_path}")
        return True

    except Exception as e:
        logger.error(f"An unexpected error occurred during CSV creation/saving for {output_csv_path}: {e}", exc_info=True)
        return False


