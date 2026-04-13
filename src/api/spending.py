from fastapi import APIRouter, HTTPException, Query
from src.models.schemas import SpendingSummary
from src.services.data_analysis import analyze_spending

router = APIRouter()


@router.get("/{user_id}", response_model=SpendingSummary)
async def get_spending_analysis(user_id: str, days: int = Query(30, ge=7, le=365)):
    try:
        analysis = analyze_spending(user_id, days=days)
        return SpendingSummary(**analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
