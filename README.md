# FastAPI Data Pipeline (Starter)

Fetch → Clean (Pandas) → Store (SQLite via SQLAlchemy) → Serve (FastAPI)

## Quickstart
```bash
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then:
- POST `http://127.0.0.1:8000/fetch` — fetch sample items (JSONPlaceholder), process, store in SQLite.
- GET  `http://127.0.0.1:8000/items` — list stored items (latest 20).
- GET  `http://127.0.0.1:8000/health` — health check.

Notes
- DB: `data/app.db` (auto-created). Change path in `app/db.py` if needed.
- Replace the fetch URL and the Pandas transform with your own logic.
