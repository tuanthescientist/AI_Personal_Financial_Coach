"""
Spending & Income Analysis Engine
─────────────────────────────────
Uses Pandas for aggregation, anomaly detection (z-score), and insight generation.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import date, timedelta


# ── Mock data generator (replace with real DB queries in production) ──────────

def fetch_user_transactions(user_id: str, days: int = 90) -> pd.DataFrame:
    """Return a realistic synthetic transaction DataFrame for demo purposes."""
    rng = np.random.default_rng(hash(user_id) % 2**31)
    dates = pd.date_range(end=date.today(), periods=days, freq="D")

    categories = ["Groceries", "Dining", "Transport", "Entertainment",
                   "Utilities", "Shopping", "Healthcare", "Education"]

    rows = []
    for d in dates:
        # 1-3 expenses per day
        n_txns = rng.integers(1, 4)
        for _ in range(n_txns):
            cat = rng.choice(categories)
            amount = -round(rng.uniform(20_000, 500_000), -3)  # VND expenses
            rows.append({"date": d, "amount": amount, "category": cat, "is_income": False})

        # Salary on the 1st of each month
        if d.day == 1:
            rows.append({
                "date": d,
                "amount": round(rng.uniform(15_000_000, 35_000_000), -3),
                "category": "Salary",
                "is_income": True,
            })

    return pd.DataFrame(rows)


# ── Core analytics ────────────────────────────────────────────────────────────

def analyze_spending(user_id: str, days: int = 30) -> Dict[str, Any]:
    df = fetch_user_transactions(user_id, days=max(days, 90))
    recent = df[df["date"] >= pd.Timestamp(date.today() - timedelta(days=days))]

    income_df = recent[recent["is_income"]]
    expense_df = recent[~recent["is_income"]]

    total_income = float(income_df["amount"].sum())
    total_expenses = float(abs(expense_df["amount"].sum()))
    net_savings = total_income - total_expenses
    savings_rate = net_savings / total_income if total_income > 0 else 0.0

    # Category breakdown
    cat_totals = abs(expense_df.groupby("category")["amount"].sum())
    categories = [
        {
            "category": cat,
            "amount": float(amt),
            "percentage": float(amt / total_expenses * 100) if total_expenses else 0,
        }
        for cat, amt in cat_totals.items()
    ]

    insights = _generate_insights(total_income, total_expenses, savings_rate, categories)
    anomalies = _detect_anomalies(expense_df)

    return {
        "user_id": user_id,
        "period": f"Last {days} days",
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_savings": net_savings,
        "savings_rate": savings_rate,
        "categories": categories,
        "insights": insights,
        "anomalies": anomalies,
    }


def _generate_insights(income: float, expenses: float, rate: float, cats: List[dict]) -> List[str]:
    insights = []
    if rate >= 0.3:
        insights.append(f"Excellent! You're saving {rate:.0%} of your income — well above the recommended 20%.")
    elif rate >= 0.1:
        insights.append(f"You're saving {rate:.0%} of income. Aim for 20 % to build a stronger safety net.")
    else:
        insights.append(f"Warning: Your savings rate is only {rate:.0%}. Consider cutting discretionary expenses.")

    top = sorted(cats, key=lambda c: -c["amount"])
    if top:
        insights.append(f"Your biggest spending category is {top[0]['category']} at {top[0]['percentage']:.0f}% of expenses.")

    if any(c["category"] == "Dining" and c["percentage"] > 25 for c in cats):
        insights.append("Dining out accounts for over 25 % of your spending — cooking at home could save significantly.")

    return insights


def _detect_anomalies(expense_df: pd.DataFrame) -> List[str]:
    """Flag daily totals > 2 standard-deviations from mean (simple z-score)."""
    if expense_df.empty:
        return []
    daily = abs(expense_df.groupby(expense_df["date"].dt.date)["amount"].sum())
    mean, std = daily.mean(), daily.std()
    if std == 0:
        return []
    anomalies = []
    for d, total in daily.items():
        z = (total - mean) / std
        if z > 2:
            anomalies.append(f"Unusual spike on {d}: {total:,.0f} VND (z={z:.1f})")
    return anomalies


# ── User profile for recommender ─────────────────────────────────────────────

def get_user_profile(user_id: str) -> Dict[str, Any]:
    analysis = analyze_spending(user_id)
    return {
        "savings_rate": analysis["savings_rate"],
        "monthly_income": analysis["total_income"],
        "top_categories": [c["category"] for c in sorted(analysis["categories"], key=lambda x: -x["amount"])[:3]],
        "risk_tolerance": "moderate",
        "active_goals": [],
    }
