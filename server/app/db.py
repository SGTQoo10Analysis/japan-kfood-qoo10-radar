import os
import sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("LOCAL_DB_PATH", "/tmp/kfood_radar.sqlite3"))

def conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def init_db():
    with conn() as c:
        c.execute("""
        CREATE TABLE IF NOT EXISTS trend_entity (
          entity_id TEXT PRIMARY KEY,
          canonical_name TEXT NOT NULL,
          japanese_names TEXT,
          category TEXT,
          created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS signal_snapshot (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          entity_id TEXT NOT NULL,
          source TEXT NOT NULL,
          metric TEXT NOT NULL,
          value REAL,
          captured_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS trend_score (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          entity_id TEXT NOT NULL,
          score REAL,
          delta_24h REAL,
          delta_7d REAL,
          confidence REAL,
          captured_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)

def save_entities(items):
    with conn() as c:
        for x in items:
            c.execute("""
            INSERT INTO trend_entity(entity_id, canonical_name, japanese_names, category)
            VALUES(?,?,?,?)
            ON CONFLICT(entity_id) DO UPDATE SET
              canonical_name=excluded.canonical_name,
              japanese_names=excluded.japanese_names,
              category=excluded.category
            """, (x["entity_id"], x["canonical_name"], x.get("japanese_names",""), x.get("category","food")))

def save_signal(entity_id, source, metric, value):
    with conn() as c:
        c.execute(
            "INSERT INTO signal_snapshot(entity_id,source,metric,value) VALUES(?,?,?,?)",
            (entity_id, source, metric, value)
        )

def get_latest_trends():
    with conn() as c:
        rows = c.execute("""
        SELECT e.entity_id, e.canonical_name, e.category,
               MAX(s.value) AS value
        FROM trend_entity e
        LEFT JOIN signal_snapshot s ON s.entity_id=e.entity_id
        GROUP BY e.entity_id
        ORDER BY value DESC
        LIMIT 100
        """).fetchall()
    return [dict(r) for r in rows]
