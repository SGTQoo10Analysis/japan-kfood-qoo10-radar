from datetime import datetime, timezone
import os

from fastapi import FastAPI, HTTPException, Header
from .collect import run_collection
from .db import init_db, get_latest_trends

app = FastAPI(title="Japan K-Food Trend Radar API", version="0.1.0")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/api/health")
def health():
    return {"ok": True, "service": "kfood-trend-api", "time": datetime.now(timezone.utc).isoformat()}

@app.get("/api/trends")
def trends(geo: str = "JP", category: str = "food"):
    return {"geo": geo, "category": category, "data": get_latest_trends()}

@app.get("/api/trends/{entity_id}")
def trend_entity(entity_id: str):
    rows = [x for x in get_latest_trends() if x["entity_id"] == entity_id]
    if not rows:
        raise HTTPException(status_code=404, detail="entity not found")
    return rows[0]

@app.post("/api/collect/run")
def collect_run(x_polling_secret: str | None = Header(default=None)):
    expected = os.getenv("POLLING_SECRET")
    if expected and x_polling_secret != expected:
        raise HTTPException(status_code=401, detail="invalid polling secret")
    return run_collection()

@app.get("/api/qoo10/competition")
def qoo10_competition(q: str = ""):
    # Qoo10 API 연동은 QOO10_API_KEY / QOO10_SELLER_AUTH_KEY 설정 후 구현.
    return {"query": q, "data": [], "status": "not_configured"}
