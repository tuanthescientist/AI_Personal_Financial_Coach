# AI Personal Financial Coach — Copilot Instructions

## Project Overview
- **Type**: Python backend + Streamlit dashboard
- **Framework**: FastAPI + Google Gemini LLM + Pandas
- **Database**: SQLAlchemy async (SQLite dev / PostgreSQL prod)

## Coding Conventions
- Use Python 3.11+ features (type hints, match statements where appropriate)
- Pydantic v2 for all request/response schemas (in src/models/schemas.py)
- Async endpoints in FastAPI routers
- All LLM prompts centralised in src/prompts/templates.py
- Loguru for logging (never use print() in production code)

## Architecture Rules
- /src/api/ — thin routers that delegate to services/agents
- /src/agents/ — LLM interaction layer (Google Gemini)
- /src/services/ — business logic and Pandas analytics
- /src/db/ — SQLAlchemy models and database session
- /dashboard/ — Streamlit UI (consumes the FastAPI endpoints)

## Running the Project
- API: `uvicorn src.main:app --reload`
- Dashboard: `streamlit run dashboard/app.py`
- Tests: `pytest`
- Docker: `docker-compose up --build`
