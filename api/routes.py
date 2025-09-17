# api/routes.py

from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from api.chat_logic import handle_chat_request

# ------------------------------------------------------------------------
# API Router for Chat Endpoints
# ------------------------------------------------------------------------
# This router handles requests related to chat completions.
# The logic for processing the request is delegated to `chat_logic.py`.
# ------------------------------------------------------------------------
router = APIRouter()

@router.post("/chat/completions")
async def chat_completions(request: Request) -> StreamingResponse:
    """
    Chat Completions Endpoint.

    - Accepts a JSON request with conversation data.
    - Delegates processing to `handle_chat_request`.
    - Returns a streaming response with model output (SSE format).
    """
    response = await handle_chat_request(request)
    return response
