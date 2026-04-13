from fastapi import APIRouter, HTTPException
from src.models.schemas import ChatRequest, ChatResponse
from src.agents.financial_coach import ask_financial_question
from src.services.data_analysis import analyze_spending

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Build context from user's spending data
        analysis = analyze_spending(request.user_id)
        context_lines = [
            f"Income: {analysis['total_income']:,.0f} VND",
            f"Expenses: {analysis['total_expenses']:,.0f} VND",
            f"Savings rate: {analysis['savings_rate']:.0%}",
        ]
        context = "\n".join(context_lines)

        result = await ask_financial_question(request.user_id, request.message, context)
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
