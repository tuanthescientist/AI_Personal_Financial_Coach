from fastapi import APIRouter, HTTPException
from typing import List
from src.models.schemas import GoalCreate, GoalResponse

router = APIRouter()

# In-memory store (replace with DB in production)
_goals: dict[str, list[dict]] = {}
_next_id = 1


@router.post("/", response_model=GoalResponse, status_code=201)
async def create_goal(goal: GoalCreate):
    global _next_id
    record = goal.model_dump()
    record["id"] = _next_id
    record["current_amount"] = 0.0
    _next_id += 1
    _goals.setdefault(goal.user_id, []).append(record)
    return GoalResponse(**record)


@router.get("/{user_id}", response_model=List[GoalResponse])
async def list_goals(user_id: str):
    return [GoalResponse(**g) for g in _goals.get(user_id, [])]
