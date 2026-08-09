# 📰 DailyBit

A daily-updated digest that pulls the latest finance, tech, and fintech articles from a curated set of reputable sources, summarizes them with AI, and explains any jargon in plain English along the way. Built for people who want to stay current without wading through dense financial or technical writing.

Every article links back to its original source — DailyBit summarizes and explains, it doesn't replace the reporting.

## ✨ Features

- **Daily auto-updating digest** — a scheduled job pulls fresh articles every day, no manual refresh needed
- **Category feeds** — Finance, Tech, and Fintech, with room to add more (e.g. Career/Industry)
- **AI-generated summaries** — each article gets a short, plain-English summary, faithful to the source text (no invented detail)
- **Inline glossary** — technical and financial terms are underlined and explain themselves on hover/tap
- **Source-linked** — every summary links to the original article
- **Top 5 per category** — curated daily, not an endless scroll

## 📡 Sources

Pulled from established, reputable outlets with free, publicly accessible RSS feeds or APIs — not aggregators or SEO content farms:

- **Finance** — Reuters (RSS), Finnhub (news API), Marketaux (news API)
- **Tech** — TechCrunch, Ars Technica, The Verge (all RSS)
- **Fintech** — Finextra, Fintech Futures, American Banker, Sifted (all RSS)

> **Note:** Bloomberg and Financial Times don't offer free RSS feeds or public APIs, so they're intentionally excluded for now. Their content is accessible via paid licensing only.

## 🛠️ Tech stack

| Layer | Choice |
|---|---|
| Frontend | React + Vite |
| Backend | Python + FastAPI |
| Database | PostgreSQL via Supabase (Python client) |
| Data validation | Pydantic |
| Scheduler | GitHub Actions (cron, with manual `workflow_dispatch` trigger) |
| Ingestion | RSS feeds (`feedparser`) / news APIs (`httpx`) |
| Summarization & keyword extraction | Azure OpenAI (`gpt-4o-mini`), validated via Pydantic structured outputs |

## 🏗️ Architecture

```
Scheduler (daily cron)
        │
        ▼
Ingestion script (Python) ── pulls latest articles per category from RSS/news APIs, fetched concurrently
        │
        ▼
LLM processing agent ── generates summary + extracts keywords, validated into Pydantic models
        │
        ├──▶ Glossary lookup ── reuses cached term definitions, or generates + caches new ones
        │
        ▼
Database (Postgres via Supabase) ── stores articles, keywords, and definitions
        │
        ▼
Backend API (FastAPI) ── serves articles and glossary terms, auto-documented at /docs
        │
        ▼
Frontend (React) ── displays category feeds with inline definitions and source links
```

## 🗄️ Database schema (draft)

Defined as Pydantic models in `server/models/articles.py`, mapped to Postgres tables:

- **articles** — `id`, `title`, `summary`, `source_url`, `source_name`, `category`, `published_at`
- **keywords** — `id`, `term`, `definition`
- **article_keywords** — `article_id`, `keyword_id` (join table)

## 📁 Project structure

```
daily-bit/
├── client/                       # React + Vite frontend
│   └── src/
│       ├── components/
│       ├── services/
│       └── App.jsx
├── server/                       # FastAPI backend
│   ├── models/
│   │   ├── __init__.py
│   │   └── articles.py           # RawArticle, Keyword, LLMOutput, Article
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ingestion.py          # per-source fetch functions + shared validation
│   │   ├── llm_agent.py          # summarization + keyword extraction
│   │   └── db.py                 # Supabase client + insert logic
│   ├── scripts/
│   │   ├── __init__.py
│   │   └── run_pipeline.py       # orchestrates the daily run
│   ├── .env
│   └── requirements.txt
└── .github/workflows/
    └── ingestion.yml
```

## 🚀 Getting started

```bash
git clone https://github.com/tomi-0/daily-bit.git
cd daily-bit

# backend
cd server
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# frontend
cd ../client
npm install
npm run dev
```

Create a `.env` file in `/server` with:

```
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
DEPLOYMENT=
MODEL_NAME=
SUPABASE_URL=
SUPABASE_KEY=
```

For the scheduled pipeline, the same values are stored as **repository secrets** (Settings → Secrets and variables → Actions) so `ingestion.yml` can inject them at run time — the workflow never reads the local `.env` file.

FastAPI's interactive docs are available at `http://localhost:8000/docs` once the backend is running.

## 🧭 Roadmap

- [x] Ingestion script pulling from RSS sources
- [x] Pydantic models for raw articles, LLM output, and stored articles
- [x] LLM summarization + keyword extraction (Azure OpenAI, structured outputs)
- [x] Daily GitHub Actions workflow with manual trigger
- [ ] Concurrent fetching across all sources (threaded ingestion + bounded async LLM calls)
- [ ] Glossary caching logic (reuse existing definitions instead of regenerating)
- [ ] Supabase write step in the pipeline
- [ ] FastAPI endpoints (`/articles`, `/glossary/{term}`)
- [ ] Frontend category feeds with keyword tooltips and "see more" expand
- [ ] Deploy (frontend + backend + Supabase)

## 📄 License

MIT
