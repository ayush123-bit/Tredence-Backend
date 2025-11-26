from fastapi import APIRouter
from app.schemas import AutocompleteRequest, AutocompleteResponse
from app.services.autocomplete_service import AutocompleteService

router = APIRouter(prefix="/api/autocomplete", tags=["autocomplete"])

@router.post("", response_model=AutocompleteResponse)
async def get_autocomplete(request: AutocompleteRequest):
    """Get AI-powered code autocomplete suggestions (mocked)"""
    service = AutocompleteService()
    suggestion = service.get_suggestion(
        request.code, 
        request.cursor_position, 
        request.language
    )
    return suggestion