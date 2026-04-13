import os
from google import genai
from google.genai import types
from loguru import logger

from src.core.config import get_settings
from src.prompts.templates import SYSTEM_PROMPT

settings = get_settings()

_client = genai.Client(api_key=settings.gemini_api_key)


async def ask_financial_question(user_id: str, question: str, context: str = "") -> dict:
    """Send a financial question to Gemini and return the response with suggestions."""
    user_message = question
    if context:
        user_message = f"[User {user_id} context]\n{context}\n\n[Question]\n{question}"

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_message)],
        ),
    ]
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.4,
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
        logger.error(f"Gemini API error: {e}")
        raise

    suggestions = _extract_suggestions(response_text)

    return {"response": response_text.strip(), "suggestions": suggestions}


def _extract_suggestions(text: str) -> list[str]:
    """Heuristically extract bullet-pointed suggestions from the LLM reply."""
    suggestions = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith(("- ", "• ", "* ", "1.", "2.", "3.")):
            suggestions.append(stripped.lstrip("-•* 0123456789.").strip())
    return suggestions[:5]
