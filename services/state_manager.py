"""SQLite persistence for interview sessions."""
from __future__ import annotations

import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import aiosqlite

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "interviews.db"


class StateManager:
    def __init__(self) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    async def init_db(self) -> None:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    data TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            await db.commit()

    async def save(self, state: dict[str, Any]) -> None:
        now = datetime.now(timezone.utc).isoformat()
        state["updated_at"] = now
        if not state.get("created_at"):
            state["created_at"] = now
        sid = state["session_id"]
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute(
                """INSERT INTO sessions (session_id, data, created_at, updated_at)
                   VALUES (?, ?, ?, ?)
                   ON CONFLICT(session_id) DO UPDATE SET
                   data=excluded.data, updated_at=excluded.updated_at""",
                (sid, json.dumps(state), state.get("created_at", now), now),
            )
            await db.commit()

    async def load(self, session_id: str) -> dict[str, Any] | None:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT data FROM sessions WHERE session_id = ?", (session_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if not row:
                    return None
                return json.loads(row["data"])

    async def list_sessions(self, limit: int = 50) -> list[dict[str, Any]]:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT data FROM sessions ORDER BY updated_at DESC LIMIT ?", (limit,)
            ) as cursor:
                rows = await cursor.fetchall()
        summaries = []
        for row in rows:
            s = json.loads(row["data"])
            summaries.append({
                "session_id": s["session_id"],
                "target_role": s.get("setup", {}).get("target_role", ""),
                "interview_type": s.get("setup", {}).get("interview_type", ""),
                "status": s.get("status", "unknown"),
                "overall_score": s.get("overall_score", 0),
                "turn_count": s.get("current_turn", 0),
                "created_at": s.get("created_at"),
            })
        return summaries

    def new_session_id(self) -> str:
        return str(uuid.uuid4())
