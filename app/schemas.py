from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RoomCreate(BaseModel):
    language: Optional[str] = "python"

class RoomResponse(BaseModel):
    room_id: str
    code: str
    language: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class AutocompleteRequest(BaseModel):
    code: str
    cursor_position: int
    language: str = "python"

class AutocompleteResponse(BaseModel):
    suggestion: str
    confidence: float

class WebSocketMessage(BaseModel):
    type: str  # "code_update", "cursor_position", "user_joined"
    content: str
    user_id: Optional[str] = None
    cursor_position: Optional[int] = None