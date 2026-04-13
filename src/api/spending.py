from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from src.services.data_analysis import analyze_spending

router = APIRouter()

class SpendingSummary(BaseModel):
    total_spent: float
    total_income: float
    categories: Dict[str, float]
    insights: list[str]

@router.get("/{user_id}", response_model=SpendingSummary)
async def get_spending_analysis(user_id: str):
    try:
        analysis = analyze_spending(user_id)
        return SpendingSummary(**analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
