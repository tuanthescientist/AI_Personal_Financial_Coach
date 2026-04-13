from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from src.agents.product_recommender import recommend_products

router = APIRouter()

class ProductRecommendation(BaseModel):
    product_name: str
    product_type: str
    reason: str
    confidence_score: float

@router.get("/{user_id}", response_model=List[ProductRecommendation])
async def get_recommendations(user_id: str):
    try:
        recommendations = await recommend_products(user_id)
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
