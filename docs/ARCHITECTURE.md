# Architecture — AI Personal Financial Coach

## System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                      SOL Banking App (Client)                    │
│                 Mobile / Web / Embedded WebView                  │
└────────────────────────────┬─────────────────────────────────────┘
                             │  REST / JSON
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                   FastAPI  Gateway  (port 8000)                  │
│                                                                  │
│  ┌──────────┐  ┌──────────────┐  ┌────────────────┐  ┌───────┐ │
│  │ /chat    │  │ /spending    │  │/recommendations│  │/goals │ │
│  └────┬─────┘  └──────┬───────┘  └────────┬───────┘  └───┬───┘ │
│       │               │                   │               │     │
│  ┌────▼─────┐  ┌──────▼───────┐  ┌────────▼───────┐      │     │
│  │Financial │  │   Pandas     │  │   Product      │      │     │
│  │Coach     │  │   Analysis   │  │   Recommender  │      │     │
│  │Agent     │  │   Engine     │  │   Agent        │      │     │
│  └────┬─────┘  └──────────────┘  └────────┬───────┘      │     │
│       │                                   │               │     │
│  ┌────▼───────────────────────────────────▼───┐    ┌──────▼───┐ │
│  │        Google Gemini LLM API               │    │ SQLite / │ │
│  │     (gemini-3.1-flash-lite-preview)        │    │ Postgres │ │
│  └────────────────────────────────────────────┘    └──────────┘ │
└──────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│              Streamlit Dashboard  (port 8501)                    │
│      Plotly charts · Chat UI · Recommendation cards              │
└──────────────────────────────────────────────────────────────────┘
```

## Data Flow

1. **User opens Financial Coach** → SOL app sends requests to FastAPI.
2. **Spending Analysis** → `data_analysis.py` aggregates transactions with Pandas, calculates KPIs, runs z-score anomaly detection.
3. **AI Chat** → User question + spending context → Gemini generates personalised answer.
4. **Product Recommendations** → User profile metrics → Gemini returns ranked JSON product list.
5. **Dashboard** → Streamlit fetches all API endpoints and renders interactive Plotly visualisations.

## Key Design Decisions

| Decision | Rationale |
|---|---|
| **Google Gemini** over OpenAI | Lower cost per token, fast streaming, strong Vietnamese language support |
| **FastAPI** | Async-first, automatic OpenAPI docs, Pydantic validation |
| **Pandas** for analytics | Battle-tested for tabular data, easy z-score anomaly detection |
| **Streamlit** for dashboard | Rapid prototyping, Python-native, no frontend build step |
| **SQLite → PostgreSQL** | Start light, swap via `DATABASE_URL` for production |
| **Prompt engineering** in `/src/prompts/` | Centralised, version-controlled, testable templates |
