from src.services.data_analysis import analyze_spending, get_user_profile, _detect_anomalies
import pandas as pd


def test_analyze_spending_keys():
    result = analyze_spending("test_user", days=30)
    assert "total_income" in result
    assert "total_expenses" in result
    assert "savings_rate" in result
    assert "categories" in result
    assert "insights" in result
    assert "anomalies" in result


def test_savings_rate_range():
    result = analyze_spending("test_user", days=30)
    assert -1.0 <= result["savings_rate"] <= 1.0


def test_categories_sum():
    result = analyze_spending("test_user", days=30)
    cat_sum = sum(c["amount"] for c in result["categories"])
    assert abs(cat_sum - result["total_expenses"]) < 1.0  # floating-point tolerance


def test_user_profile():
    profile = get_user_profile("test_user")
    assert "savings_rate" in profile
    assert "monthly_income" in profile
    assert "top_categories" in profile


def test_anomaly_detection_empty():
    empty_df = pd.DataFrame(columns=["date", "amount"])
    assert _detect_anomalies(empty_df) == []
