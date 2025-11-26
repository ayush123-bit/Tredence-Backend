from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models import RoomModel
from datetime import datetime
import uuid

class RoomService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.rooms
    
    async def create_room(self, language: str = "python") -> dict:
        """Create a new room with a unique ID"""
        room_id = str(uuid.uuid4())[:8]
        
        # Ensure uniqueness
        while await self.collection.find_one({"room_id": room_id}):
            room_id = str(uuid.uuid4())[:8]
        
        room_data = {
            "room_id": room_id,
            "language": language,
            "code": f"# Welcome to room {room_id}\n# Start coding here...\n",
            "created_at": datetime.utcnow(),
            "updated_at": None
        }
        
        result = await self.collection.insert_one(room_data)
        room_data["_id"] = str(result.inserted_id)
        
        return room_data
    
    async def get_room(self, room_id: str) -> dict:
        """Get room by ID"""
        room = await self.collection.find_one({"room_id": room_id})
        if room:
            room["_id"] = str(room["_id"])
        return room
    
    async def update_room_code(self, room_id: str, code: str) -> dict:
        """Update the code in a room"""
        result = await self.collection.update_one(
            {"room_id": room_id},
            {
                "$set": {
                    "code": code,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        if result.modified_count > 0:
            return await self.get_room(room_id)
        return None
    
    async def delete_room(self, room_id: str) -> bool:
        """Delete a room"""
        result = await self.collection.delete_one({"room_id": room_id})
        return result.deleted_count > 0
    
    async def list_rooms(self, limit: int = 50) -> list:
        """List all rooms"""
        cursor = self.collection.find().sort("created_at", -1).limit(limit)
        rooms = await cursor.to_list(length=limit)
        
        for room in rooms:
            room["_id"] = str(room["_id"])
        
        return rooms