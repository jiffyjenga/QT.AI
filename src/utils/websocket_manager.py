from fastapi.websockets import WebSocket
from typing import Dict, List, Any
import json
import asyncio

class ConnectionManager:
    def __init__(self):
        # Store active connections by channel
        self.active_connections: Dict[str, List[WebSocket]] = {
            "market": [],
            "trades": [],
        }
    
    async def connect(self, websocket: WebSocket, channel: str):
        """Connect a client to a specific channel"""
        await websocket.accept()
        if channel not in self.active_connections:
            self.active_connections[channel] = []
        self.active_connections[channel].append(websocket)
    
    def disconnect(self, websocket: WebSocket, channel: str):
        """Disconnect a client from a specific channel"""
        if channel in self.active_connections:
            if websocket in self.active_connections[channel]:
                self.active_connections[channel].remove(websocket)
    
    async def broadcast(self, message: Any, channel: str):
        """Broadcast a message to all connected clients in a channel"""
        if channel not in self.active_connections:
            return
        
        # Convert message to JSON if it's not already a string
        if not isinstance(message, str):
            message = json.dumps(message)
        
        # Send to all connected clients
        for connection in self.active_connections[channel]:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error broadcasting to client: {e}")
                # Remove the connection if it's broken
                self.active_connections[channel].remove(connection)
    
    async def send_personal_message(self, message: Any, websocket: WebSocket):
        """Send a message to a specific client"""
        # Convert message to JSON if it's not already a string
        if not isinstance(message, str):
            message = json.dumps(message)
        
        try:
            await websocket.send_text(message)
        except Exception as e:
            print(f"Error sending personal message: {e}")
