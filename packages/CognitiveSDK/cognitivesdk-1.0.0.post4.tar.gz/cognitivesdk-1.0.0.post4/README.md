# CognitiveSDK Documentation: System Architecture and Data Flow

## Overview

CognitiveSDK is a flexible framework designed for real-time data acquisition and streaming from various input devices and sensors. It provides a modular architecture for connecting to devices (like Muse-S, Emotibit, MetaGlass), transmitting their data through a queuing system, and processing that data in real-time applications.

The core of the framework uses a distributed publish-subscribe (XPub/XSub) pattern built on ZeroMQ, allowing multiple components to share data efficiently across processes or even different machines on a network.

CognitiveSDK implements automatic sensor management that creates dedicated Subdevices for each sensor on a physical device. For example, when connecting to a device with EEG, PPG, and MAG sensors, CognitiveSDK automatically creates three dedicated subdevices—one for each sensor type. Each subdevice functions as a ZeroMQ Publisher, contributing data to the central queuing system.

The SDK leverages ZeroMQ's topic-based messaging system, where each publisher (subdevice) is assigned a unique topic. This allows users to subscribe to specific data streams using a hierarchical naming convention. For example, if a device named "my_device" has EEG, PPG, and MAG sensors, users can subscribe to "my_device.EEG", "my_device.PPG", or "my_device.MAG" to access each specific data stream.

## System Architecture Diagram

The following diagram illustrates the overall architecture of CognitiveSDK, showing how data flows from devices through the system:

![CognitiveSDK Architecture](arch.png)

The diagram shows the relationship between devices, subdevices, the messaging system, and how applications can consume the data through subscribers.

## Core Architecture

The system consists of several key components:

1.  **Device Layer**: Connects to physical devices and loads their configurations.
2.  **Subdevice Layer**: Handles specific data streams from devices (e.g., EEG, PPG, Video).
3.  **Middleware Layer**: Provides adapters for different device communication protocols (BrainFlow, LSL, Synthetic, etc.).
4.  **Messaging Layer**: Uses ZeroMQ for efficient publish-subscribe data distribution.
5.  **Metadata Responder**: Implements a ZeroMQ Rep/Req pattern to provide metadata about currently streaming devices.
6.  **Shared State**: Manages runtime configuration and status.
7.  **External Subscribers**: Allows integration of custom data processing modules.

## Data Flow

1.  **Physical Device → Middleware Interface**
    *   Middleware interfaces (e.g., `BrainflowInterface`, `SyntheticInterface`, custom implementations) connect to physical or virtual devices.
    *   Raw data samples are acquired according to the device protocol and buffered based on the `EpochLength` parameter.
2.  **Middleware Interface → SubDevice → Publisher**
    *   The middleware's `_read_loop` processes buffered data chunks.
    *   For each `SubDevice` associated with the `Device`, the middleware extracts the relevant data channels (using `ChannelsIndex` from the preset).
    *   The extracted data chunk is passed to the corresponding `SubDevice`'s `on_data` method.
    *   The `SubDevice` forwards the data to its internal `Publisher` instance.
    *   The `Publisher` serializes the data into the standard JSON format (including sequence number and timestamp) and sends it to the ZeroMQ proxy.
3.  **Publisher → ZeroMQ Proxy → Subscribers**
    *   Publishers send JSON messages to a central `XPubXSubProxy` on specific topics (e.g., "MuseDeviceA.EEG", "SynthDevice.EEG").
    *   The proxy distributes messages to all interested subscribers based on their topic subscriptions.
4.  **Subscribers → Applications**
    *   Subscribers (like the built-in `LocalCacheManager` or custom external subscribers) receive the topic and JSON payload.
    *   Subscribers parse the JSON data and invoke user-defined callbacks or perform other actions (e.g., saving to disk, processing).

## Configuration System (`main.yaml` & Presets)

The primary configuration is handled through `main.yaml`, loaded into `SharedState` at startup. This file defines global settings and points to device-specific configurations stored in JSON preset files located in `src/CognitiveSDK/presets/`.

*   **`main.yaml`:** Defines global settings (stream duration, external control), lists external subscribers, and configures specific device instances (assigning a unique name, selecting a preset, choosing middleware, overriding parameters like serial number).
*   **Preset Files (`*.json`):** Define the capabilities of a device *type*, including available middleware options and the subdevice streams (channels, sampling rates) provided by each middleware.

For detailed structure information, see:
*   [**Data Structures Guide**](./doc/data_structures.md)

## Extending CognitiveSDK

The framework is designed for extension:

*   **Adding New Devices:** You can add support for new hardware by creating a preset file, implementing a middleware interface, and updating the configuration.
    *   See: [**Adding a New Device Guide**](./doc/adding_new_device.md)

*   **Creating Custom Subscribers:** Integrate your own data processing, analysis, or visualization logic by creating external subscriber modules.
    *   See: [**Creating Custom Subscribers Guide**](./doc/custom_subscriber.md)

*   **Controlling Data Publication:** Implement external control logic to start, stop, pause, or resume data streams from publishers programmatically.
    *   See: [**Controlling Data Publication Externally Guide**](./doc/controlling_publishers.md)

## Key Components (Brief)

*   **`Device` / `DeviceManager`:** Manages connection and lifecycle of individual hardware/virtual devices.
*   **`SubDevice`:** Represents a single data stream (e.g., EEG) from a `Device`.
*   **Middleware (`BrainflowInterface`, `SyntheticInterface`, etc.):** Adapters for specific device communication protocols.
*   **`XPubXSubProxy`:** Central ZeroMQ message broker.
*   **`Publisher`:** Sends data from a `SubDevice` to the proxy.
*   **`DataSubscriber`:** Base class for receiving data from the proxy.
*   **`MetadataResponder`:** Provides runtime state information via ZMQ REQ/REP.
*   **`SharedState`:** Singleton holding merged configuration and dynamic state.
*   **`Orcustrator`:** Singleton managing the lifecycle of core components (Proxy, MetadataResponder) and external subscribers.

## Supported Device Types

The framework currently includes presets and middleware for:

1.  **Muse-S** (via BrainFlow)
    *   EEG
    *   PPG
    *   Accelerometer
2.  **Synthetic** (Built-in data generator)
    *   EEG (configurable bands, noise, etc.)

Support for other devices (e.g., OpenBCI, Emotibit) can be added by following the [Adding a New Device Guide](./doc/adding_new_device.md).

## Installation

```bash
pip install cognitivesdk=1.0.0.post3
```

## Usage

1.  **Configure `main.yaml`:** Define your devices, select middleware, and configure global settings.
2.  **Run the main script:**
    ```bash
    python main.py [--debug]
    ```
