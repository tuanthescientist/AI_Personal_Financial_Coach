import json
from google import genai
from google.genai import types
from loguru import logger

from src.core.config import get_settings
from src.prompts.templates import SYSTEM_PROMPT, PRODUCT_RECOMMENDATION_PROMPT
from src.services.data_analysis import analyze_spending, get_user_profile

settings = get_settings()
_client = genai.Client(api_key=settings.gemini_api_key)


async def recommend_products(user_id: str) -> list[dict]:
    """Use spending analysis + Gemini to generate personalised product recommendations."""
    profile = get_user_profile(user_id)
    analysis = analyze_spending(user_id)

    prompt_text = PRODUCT_RECOMMENDATION_PROMPT.format(
        savings_rate=analysis["savings_rate"],
        top_categories=", ".join(
            f"{c['category']} ({c['percentage']:.0f}%)"
            for c in sorted(analysis["categories"], key=lambda x: -x["amount"])[:3]
        ),
        monthly_income=analysis["total_income"],
        risk_tolerance=profile.get("risk_tolerance", "moderate"),
        goals=", ".join(profile.get("active_goals", [])) or "None set",
    )

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt_text)],
        ),
    ]
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.3,
        max_output_tokens=1024,
    )

    response_text = ""
    try:
        for chunk in _client.models.generate_content_stream(
            model=settings.gemini_model,
            contents=contents,
            config=config,
        ):
            if chunk.text:
                response_text += chunk.text
    except Exception as e:
        logger.error(f"Gemini recommendation error: {e}")
        raise

    return _parse_recommendations(response_text)


def _parse_recommendations(text: str) -> list[dict]:
    """Parse JSON array from LLM output, with fallback."""
    try:
        start = text.index("[")
        end = text.rindex("]") + 1
        return json.loads(text[start:end])
    except (ValueError, json.JSONDecodeError):
        logger.warning("Could not parse LLM recommendation JSON — returning empty list")
        return []
