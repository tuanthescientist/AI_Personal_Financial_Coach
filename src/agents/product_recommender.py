from src.services.data_analysis import get_user_profile

async def recommend_products(user_id: str) -> list:
    """Recommend bank products based on user profile and recent spending."""
    profile = get_user_profile(user_id)
    
    products = []
    
    # Simple logic placeholder for product recommendations using GenAI
    if profile.get("savings_ratio", 0) < 0.2:
        products.append({
            "product_name": "Automatic Savings Plan",
            "product_type": "Savings",
            "reason": "We noticed your savings ratio is below 20%. Automating savings can help build your emergency fund faster.",
            "confidence_score": 0.85
        })
    elif profile.get("has_high_credit_utilization", False):
        products.append({
            "product_name": "SOL Low APR Credit Card Consolidation",
            "product_type": "Credit",
            "reason": "Lower your monthly payments by consolidating high-interest credit card debt.",
            "confidence_score": 0.90
        })
    
    return products
