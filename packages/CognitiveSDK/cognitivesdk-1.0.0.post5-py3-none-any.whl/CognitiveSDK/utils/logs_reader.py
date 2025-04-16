import time
import os
import asyncio
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler
from CognitiveSDK.utils.socketio_log_streamer import WebSocketServer

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, websocket_server):
        self.file_offsets = {}
        self.websocket_server = websocket_server

    def on_modified(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        file_name = os.path.basename(file_path)

        # Get previous offset or start at 0
        offset = self.file_offsets.get(file_path, 0)

        try:
            with open(file_path, 'r') as f:
                f.seek(offset)
                new_content = f.read()
                if new_content:
                    print(f"\n--- Publishing changes in {file_path} ---")
                    print(new_content.strip())
                    self.file_offsets[file_path] = f.tell()

                    # Publish the changes over WebSocket
                    asyncio.run(self.websocket_server.publish_message(event="LOG_MODIFIED", data={"file": file_name,"log":new_content.strip()}))
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    def on_created(self, event):
        if not event.is_directory:
            self.file_offsets[event.src_path] = 0
            print(f'Created: {event.src_path}')
            # asyncio.run(self.websocket_server.publish_message(event="LOG_CREATED", data=event.src_path ))

    def on_deleted(self, event):
        if not event.is_directory:
            self.file_offsets.pop(event.src_path, None)
            print(f'Deleted: {event.src_path}')
            # asyncio.run(self.websocket_server.publish_message(f"File deleted: {event.src_path}"))

    def on_moved(self, event):
        if not event.is_directory:
            self.file_offsets.pop(event.src_path, None)
            print(f'Moved: {event.src_path} to {event.dest_path}')
            # asyncio.run(self.websocket_server.publish_message(f"File moved: {event.src_path} to {event.dest_path}"))

async def main():
    # Start the WebSocket server
    websocket_server = WebSocketServer()
    websocket_task = asyncio.create_task(websocket_server.start())

    # Start the file observer
    path = "../../../logs"
    event_handler = ChangeHandler(websocket_server)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    observer.start()
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

    # Stop the WebSocket server
    websocket_task.cancel()
    try:
        await websocket_task
    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    asyncio.run(main())