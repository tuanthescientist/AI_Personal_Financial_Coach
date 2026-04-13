"""Seed the SQLite database with realistic demo transactions."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import numpy as np
from datetime import date, timedelta
from src.db.database import init_db, async_session
from src.db.models import Transaction, UserProfile


async def seed():
    await init_db()

    rng = np.random.default_rng(42)
    user_id = "demo_user_001"

    categories = ["Groceries", "Dining", "Transport", "Entertainment",
                   "Utilities", "Shopping", "Healthcare", "Education"]

    async with async_session() as session:
        # Create user profile
        profile = UserProfile(
            user_id=user_id,
            monthly_income=25_000_000,
            risk_tolerance="moderate",
        )
        session.add(profile)

        # 90 days of transactions
        for i in range(90):
            d = date.today() - timedelta(days=90 - i)

            for _ in range(rng.integers(1, 4)):
                cat = rng.choice(categories)
                amount = -round(float(rng.uniform(20_000, 500_000)), -3)
                session.add(Transaction(
                    user_id=user_id, date=d, amount=amount,
                    category=cat, is_income=False,
                ))

            if d.day == 1:
                salary = round(float(rng.uniform(20_000_000, 30_000_000)), -3)
                session.add(Transaction(
                    user_id=user_id, date=d, amount=salary,
                    category="Salary", is_income=True,
                ))

        await session.commit()
    print(f"✅  Seeded database for user '{user_id}'")


if __name__ == "__main__":
    asyncio.run(seed())
