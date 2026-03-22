import logging
import traceback
from fastapi import APIRouter, Depends, HTTPException

from app.api.schemas.chat import ChatRequest
from app.application.use_cases.chat_with_documents import chat_with_documents_use_case
from app.dependencies import get_chat_service

router = APIRouter()
logger = logging.getLogger("chat")


@router.post("/api/chat")
def chat_with_documents(
    request: ChatRequest,
    chat_service=Depends(get_chat_service),
):
    try:
        return chat_with_documents_use_case(
            chat_service=chat_service,
            question=request.question,
            top_k=request.top_k,
        )
    except Exception as ex:
        logger.exception("Chat endpoint failed")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(ex))