from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.agents.financial_coach import ask_financial_question

router = APIRouter()

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        response_text = await ask_financial_question(request.user_id, request.message)
        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
