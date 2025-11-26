from fastapi import APIRouter, HTTPException, Depends
from app.schemas import RoomCreate, RoomResponse
from app.services.room_service import RoomService
from app.database import get_database

router = APIRouter(prefix="/api/rooms", tags=["rooms"])

@router.post("", response_model=RoomResponse)
async def create_room(room: RoomCreate, db=Depends(get_database)):
    """Create a new collaborative coding room"""
    room_service = RoomService(db)
    new_room = await room_service.create_room(room.language)
    return new_room

@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(room_id: str, db=Depends(get_database)):
    """Get room details by room ID"""
    room_service = RoomService(db)
    room = await room_service.get_room(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.put("/{room_id}/code")
async def update_room_code(room_id: str, code: dict, db=Depends(get_database)):
    """Update room code"""
    room_service = RoomService(db)
    updated_room = await room_service.update_room_code(room_id, code.get("code", ""))
    if not updated_room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"status": "success", "room_id": room_id}