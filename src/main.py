from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.api import chat, spending, recommendations, goals
from src.core.config import get_settings
from src.db.database import init_db

settings = get_settings()

app = FastAPI(
    title="AI Personal Financial Coach API",
    description=(
        "Production-grade backend for the AI Personal Financial Coach "
        "embedded in the SOL banking app. Analyses spending/income patterns "
        "using Pandas, generates proactive product recommendations and "
        "answers financial questions via Google Gemini LLM."
    ),
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(spending.router, prefix="/api/v1/spending", tags=["Spending Analysis"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["Product Recommendations"])
app.include_router(goals.router, prefix="/api/v1/goals", tags=["Financial Goals"])


@app.on_event("startup")
async def startup():
    logger.info("Initialising database …")
    await init_db()
    logger.info("AI Personal Financial Coach API is ready.")


@app.get("/health", tags=["System"])
def health_check():
    return {"status": "ok", "version": "2.0.0"}
