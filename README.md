# 📰 DailyBit

A daily-updated digest that pulls the latest finance, tech, and fintech articles from a curated set of reputable sources, summarizes them with AI, and explains any jargon in plain English along the way. Built for people who want to stay current without wading through dense financial or technical writing.

Every article links back to its original source — DailyBit summarizes and explains, it doesn't replace the reporting.

## ✨ Features

- **Daily auto-updating digest** — a scheduled job pulls fresh articles every day, no manual refresh needed
- **Category feeds** — Finance, Tech, and Fintech, with room to add more (e.g. Career/Industry)
- **AI-generated summaries** — each article gets a short, plain-English summary
- **Inline glossary** — technical and financial terms are underlined and explain themselves on hover/tap
- **Source-linked** — every summary links to the original article
- **Top 5 per category** — curated daily, not an endless scroll

## 📡 Sources

Pulled from established, reputable outlets — not aggregators or SEO content farms:

- **Finance** — Reuters, Bloomberg, Financial Times
- **Tech** — TechCrunch, Ars Technica, The Verge
- **Fintech** — Fintech Futures, American Banker, Sifted

## 🛠️ Tech stack

| Layer | Choice |
|---|---|
| Frontend | React + Vite |
| Backend | Python + FastAPI |
| Database | PostgreSQL via Supabase (Python client) |
| Data validation | Pydantic |
| Scheduler | GitHub Actions (cron) |
| Ingestion | RSS feeds / news APIs (`feedparser` or `httpx`) |
| Summarization & keyword extraction | LLM API (Claude/OpenAI) |

## 🏗️ Architecture

```
Scheduler (daily cron)
        │
        ▼
Ingestion script (Python) ── pulls latest articles per category from RSS/news APIs
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

Defined as Pydantic models in `server/app/models/schemas.py`, mapped to Postgres tables:

- **articles** — `id`, `title`, `summary`, `source_url`, `source_name`, `category`, `published_at`
- **keywords** — `id`, `term`, `definition`
- **article_keywords** — `article_id`, `keyword_id` (join table)

## 📁 Project structure

```
dailybit/
├── client/            # React + Vite frontend
│   └── src/
│       ├── components/
│       ├── api/
│       └── App.jsx
├── server/            # FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── models/
│   │   ├── services/
│   │   └── db/
│   └── scripts/
│       └── run_daily_pipeline.py
└── .github/workflows/
    └── daily-digest.yml
```

## 🚀 Getting started

```bash
git clone <repo-url>
cd dailybit

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
SUPABASE_URL=
SUPABASE_KEY=
LLM_API_KEY=
```

FastAPI's interactive docs are available at `http://localhost:8000/docs` once the backend is running.

## 🧭 Roadmap

- [ ] Ingestion service pulling from chosen RSS sources
- [ ] LLM summarization + keyword extraction pipeline
- [ ] Glossary caching logic
- [ ] Daily GitHub Actions workflow
- [ ] Frontend category feeds with keyword tooltips
- [ ] Deploy (frontend + backend + Supabase)

## 📄 License

MIT