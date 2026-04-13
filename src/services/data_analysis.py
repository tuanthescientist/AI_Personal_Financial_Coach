import pandas as pd
from typing import Dict, Any
import numpy as np

def fetch_user_transactions(user_id: str) -> pd.DataFrame:
    """Mock database query fetching user's transaction history."""
    dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
    data = {
        "date": dates,
        "amount": np.random.uniform(-150, 200, size=30),
        "category": np.random.choice(["Groceries", "Dining", "Entertainment", "Salary", "Utilities"], size=30)
    }
    df = pd.DataFrame(data)
    
    # Simple fix to ensure Salary is always positive
    df.loc[df['category'] == 'Salary', 'amount'] = np.abs(df.loc[df['category'] == 'Salary', 'amount']) * 15
    return df

def analyze_spending(user_id: str) -> Dict[str, Any]:
    """Analyzes a user's recent spending/income patterns."""
    df = fetch_user_transactions(user_id)
    
    income_df = df[df['amount'] > 0]
    expenses_df = df[df['amount'] < 0]
    
    total_income = income_df['amount'].sum()
    total_spent = abs(expenses_df['amount'].sum())
    
    # Calculate category expenses
    categories = abs(expenses_df.groupby('category')['amount'].sum()).to_dict()
    
    # Generate insights
    insights = []
    if total_spent > total_income:
        insights.append(f"Careful! You spent ${total_spent - total_income:.2f} more than you earned this period.")
    else:
        insights.append(f"Great job saving! You have a surplus of ${total_income - total_spent:.2f} this period.")
        
    if categories.get('Dining', 0) > (total_spent * 0.3):
        insights.append("Your dining expenses take up over 30% of your budget. Consider cooking at home to save money.")
        
    return {
        "total_spent": total_spent,
        "total_income": total_income,
        "categories": categories,
        "insights": insights
    }

def get_user_profile(user_id: str) -> Dict[str, Any]:
    """Calculate aggregated metrics to inform the recommender system."""
    analysis = analyze_spending(user_id)
    savings = max(analysis['total_income'] - analysis['total_spent'], 0)
    
    savings_ratio = savings / analysis['total_income'] if analysis['total_income'] > 0 else 0
    
    return {
        "savings_ratio": savings_ratio,
        "has_high_credit_utilization": False, # Mock value
        "recent_category_flags": [cat for cat, val in analysis['categories'].items() if val > 500]
    }
