import asyncio
import json
import websockets

class WebSocketServer:
    def __init__(self, host="localhost", port=6789):
        self.host = host
        self.port = port
        self.connected_clients = set()

    async def handler(self, websocket):
        self.connected_clients.add(websocket)
        print(f"Client connected: {websocket.remote_address}")
        try:
            async for message in websocket:
                print(f"Received from client: {message}")
        except websockets.exceptions.ConnectionClosed:
            print(f"Client disconnected: {websocket.remote_address}")
        finally:
            self.connected_clients.remove(websocket)

    async def publish_message(self, event: str, data: str):
        message = json.dumps({
            "event": event,
            "data": data
        })
        if self.connected_clients:
            await asyncio.gather(*[client.send(message) for client in self.connected_clients])
            print(f"Published: {message}")
        else:
            print("No clients to send to.")

    async def start(self):
        async with websockets.serve(self.handler, self.host, self.port):
            print(f"WebSocket server running at ws://{self.host}:{self.port}")
            await asyncio.Future()  # Keep the server running indefinitely