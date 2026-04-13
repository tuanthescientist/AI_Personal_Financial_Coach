from fastapi import APIRouter, HTTPException
from typing import List
from src.models.schemas import ProductRecommendation
from src.agents.product_recommender import recommend_products

router = APIRouter()


@router.get("/{user_id}", response_model=List[ProductRecommendation])
async def get_recommendations(user_id: str):
    try:
        recommendations = await recommend_products(user_id)
        return [ProductRecommendation(**r) for r in recommendations]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
