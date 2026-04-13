from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import chat, spending, recommendations

app = FastAPI(
    title="AI Personal Financial Coach API",
    description="Backend services for the AI Personal Financial Coach embedded in SOL app",
    version="1.0.0"
)

# CORS middleware for SOL app integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(spending.router, prefix="/api/v1/spending", tags=["Spending"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["Recommendations"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
