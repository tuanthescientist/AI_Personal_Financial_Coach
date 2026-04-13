from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


# ── Chat ──────────────────────────────────────────────
class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    suggestions: List[str] = Field(default_factory=list)


# ── Transactions ──────────────────────────────────────
class TransactionCreate(BaseModel):
    user_id: str
    date: date
    amount: float
    category: str
    description: str = ""
    is_income: bool = False

class TransactionResponse(TransactionCreate):
    id: int

    class Config:
        from_attributes = True


# ── Spending Analysis ─────────────────────────────────
class CategoryBreakdown(BaseModel):
    category: str
    amount: float
    percentage: float

class SpendingSummary(BaseModel):
    user_id: str
    period: str
    total_income: float
    total_expenses: float
    net_savings: float
    savings_rate: float
    categories: List[CategoryBreakdown]
    insights: List[str]
    anomalies: List[str] = Field(default_factory=list)


# ── Product Recommendations ──────────────────────────
class ProductRecommendation(BaseModel):
    product_name: str
    product_type: str
    reason: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    priority: str = "medium"  # low / medium / high


# ── Financial Goals ──────────────────────────────────
class GoalCreate(BaseModel):
    user_id: str
    goal_name: str
    target_amount: float
    deadline: Optional[date] = None

class GoalResponse(GoalCreate):
    id: int
    current_amount: float = 0.0

    class Config:
        from_attributes = True

class GoalProgress(BaseModel):
    goal_name: str
    target_amount: float
    current_amount: float
    progress_pct: float
    on_track: bool
    monthly_required: float
