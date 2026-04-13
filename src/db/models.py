from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Boolean
from datetime import datetime, date
from src.db.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, index=True, nullable=False)
    date = Column(Date, nullable=False, default=date.today)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, default="")
    is_income = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserGoal(Base):
    __tablename__ = "user_goals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, index=True, nullable=False)
    goal_name = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    current_amount = Column(Float, default=0.0)
    deadline = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    monthly_income = Column(Float, default=0.0)
    risk_tolerance = Column(String, default="moderate")  # low / moderate / high
    created_at = Column(DateTime, default=datetime.utcnow)
