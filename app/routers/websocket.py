from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import json
from datetime import datetime

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = set()
        self.active_connections[room_id].add(websocket)
        
        # Send welcome message
        await websocket.send_json({
            "type": "connected",
            "content": f"Connected to room {room_id}",
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            self.active_connections[room_id].discard(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
    
    async def broadcast(self, message: dict, room_id: str, exclude: WebSocket = None):
        if room_id in self.active_connections:
            disconnected = set()
            for connection in self.active_connections[room_id]:
                if connection != exclude:
                    try:
                        await connection.send_json(message)
                    except:
                        disconnected.add(connection)
            
            # Clean up disconnected clients
            for conn in disconnected:
                self.disconnect(conn, room_id)
    
    def get_room_user_count(self, room_id: str) -> int:
        """Get number of connected users in a room"""
        return len(self.active_connections.get(room_id, set()))

manager = ConnectionManager()

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(websocket, room_id)
    
    # Notify others that a user joined
    await manager.broadcast({
        "type": "user_joined",
        "content": "A user has joined the room",
        "user_count": manager.get_room_user_count(room_id)
    }, room_id, exclude=websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Add timestamp to message
            message["timestamp"] = datetime.utcnow().isoformat()
            
            # Broadcast to all users in the room except sender
            await manager.broadcast(message, room_id, exclude=websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        await manager.broadcast({
            "type": "user_left",
            "content": "A user has left the room",
            "user_count": manager.get_room_user_count(room_id)
        }, room_id)