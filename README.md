# AI Personal Financial Coach Backend

This backend project implements the AI Personal Financial Coach APIs to be embedded into the SOL banking app. It leverages GenAI (LangChain, OpenAI) and Pandas for automated personal finance analysis, spending tracking, and product recommendations.

## Directory Structure

- `src/api` - FastAPI routers exposing endpoints.
- `src/agents` - LangChain LLM integrations for intelligent chat and product recommendation based on context.
- `src/services` - Pandas-based analytics pipelines to aggregate user income and spending.
- `src/models` - Pydantic definitions for request/response schemas.
- `src/core` - App configuration.

## Getting Started

1. Create a virtual environment and install dependencies:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

2. Add your environment variables in `.env`:
```
OPENAI_API_KEY=your_key_here
```

3. Run the development server:
```bash
uvicorn src.main:app --reload
```

## Running Tests
```bash
pytest
```
