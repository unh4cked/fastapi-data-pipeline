from __future__ import annotations

import os
from typing import List

import httpx
import pandas as pd
from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from .db import Base, engine, SessionLocal
from .models import Item
from .schemas import ItemOut

app = FastAPI(title="FastAPI Data Pipeline")

# Create tables
Base.metadata.create_all(bind=engine)

SAMPLE_URL = os.getenv("PIPELINE_SOURCE", "https://jsonplaceholder.typicode.com/posts?_limit=10")

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}

@app.post("/fetch")
def fetch_and_store() -> dict:
    # Fetch
    r = httpx.get(SAMPLE_URL, timeout=20.0)
    r.raise_for_status()
    data = r.json()

    # Clean/transform with Pandas (simple example)
    df = pd.DataFrame(data)
    # rename columns to a standard schema
    df = df.rename(columns={"id": "ext_id", "userId": "user_id"})
    df = df[["ext_id", "title", "body", "user_id"]]

    items: list[Item] = []
    with SessionLocal() as session:
        for row in df.to_dict(orient="records"):
            item = Item(
                ext_id=row.get("ext_id"),
                title=(row.get("title") or "")[:300],
                body=(row.get("body") or "")[:2000],
                user_id=row.get("user_id"),
            )
            session.add(item)
            items.append(item)
        session.commit()

    return {"inserted": len(items)}

@app.get("/items", response_model=List[ItemOut])
def list_items(limit: int = 20) -> List[ItemOut]:
    with SessionLocal() as session:
        stmt = select(Item).order_by(Item.id.desc()).limit(limit)
        rows = session.execute(stmt).scalars().all()
        return rows
