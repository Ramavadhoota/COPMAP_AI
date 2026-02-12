# CopMap PoC (FastAPI + SQLite + Chroma RAG)

## What works
- Create alerts (POST /api/v1/alerts)
- Live alerts over WebSocket (/ws/officers/{officer_id})
- Start/end patrol, auto-generate summary (Groq if configured, otherwise fallback)
- RAG: ingest SOP/docs and query via Chroma (persisted to ./data/chroma)

## Quickstart (local)
1) Create venv + install
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt

2) Copy env
   cp .env.example .env

3) Seed demo data (officers + SOP ingest)
   python scripts/seed_demo.py

4) Run API
   uvicorn app.main:app --reload --port 8000

Open docs:
- http://localhost:8000/docs

## Demo flow
A) Connect WebSocket (use a WS client):
   ws://localhost:8000/ws/officers/officer_1

B) Create an alert:
   POST http://localhost:8000/api/v1/alerts
   body from data/samples/alert.json

C) Start patrol:
   POST /api/v1/patrols/start

D) End patrol (auto summary):
   POST /api/v1/patrols/{patrol_id}/end

E) Query RAG:
   POST /api/v1/rag/query

## Docker
docker compose up --build
