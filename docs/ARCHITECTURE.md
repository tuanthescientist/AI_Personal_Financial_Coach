# Architecture â€” AI Personal Financial Coach

## System Overview

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                      SOL Banking App (Client)                    â”‚
â”‚                 Mobile / Web / Embedded WebView                  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                             â”‚  REST / JSON
                             â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚                   FastAPI  Gateway  (port 8000)                  â”‚
â”‚                                                                  â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â” â”‚
â”‚  â”‚ /chat    â”‚  â”‚ /spending    â”‚  â”‚/recommendationsâ”‚  â”‚/goals â”‚ â”‚
â”‚  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”¬â”€â”€â”€â”˜ â”‚
â”‚       â”‚               â”‚                   â”‚               â”‚     â”‚
â”‚  â”Œâ”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”      â”‚     â”‚
â”‚  â”‚Financial â”‚  â”‚   Pandas     â”‚  â”‚   Product      â”‚      â”‚     â”‚
â”‚  â”‚Coach     â”‚  â”‚   Analysis   â”‚  â”‚   Recommender  â”‚      â”‚     â”‚
â”‚  â”‚Agent     â”‚  â”‚   Engine     â”‚  â”‚   Agent        â”‚      â”‚     â”‚
â”‚  â””â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â””â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”˜      â”‚     â”‚
â”‚       â”‚                                   â”‚               â”‚     â”‚
â”‚  â”Œâ”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”    â”Œâ”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â” â”‚
â”‚  â”‚        Google Gemini LLM API               â”‚    â”‚ SQLite / â”‚ â”‚
â”‚  â”‚     (gemini-3.1-flash-lite-preview)        â”‚    â”‚ Postgres â”‚ â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜ â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                             â”‚
                             â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚              Streamlit Dashboard  (port 8501)                    â”‚
â”‚      Plotly charts Â· Chat UI Â· Recommendation cards              â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

## Data Flow

1. **User opens Financial Coach** â†’ SOL app sends requests to FastAPI.
2. **Spending Analysis** â†’ `data_analysis.py` aggregates transactions with Pandas, calculates KPIs, runs z-score anomaly detection.
3. **AI Chat** â†’ User question + spending context â†’ Gemini generates personalised answer.
4. **Product Recommendations** â†’ User profile metrics â†’ Gemini returns ranked JSON product list.
5. **Dashboard** â†’ Streamlit fetches all API endpoints and renders interactive Plotly visualisations.

## Key Design Decisions

| Decision | Rationale |
|---|---|
| **Google Gemini** over OpenAI | Lower cost per token, fast streaming, strong Vietnamese language support |
| **FastAPI** | Async-first, automatic OpenAPI docs, Pydantic validation |
| **Pandas** for analytics | Battle-tested for tabular data, easy z-score anomaly detection |
| **Streamlit** for dashboard | Rapid prototyping, Python-native, no frontend build step |
| **SQLite â†’ PostgreSQL** | Start light, swap via `DATABASE_URL` for production |
| **Prompt engineering** in `/src/prompts/` | Centralised, version-controlled, testable templates |

