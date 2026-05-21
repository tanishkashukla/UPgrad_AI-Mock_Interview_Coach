"""SQLite persistence for InterviewPilot sessions."""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import aiosqlite

ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "sessions.db"


class SessionDatabase:
    def __init__(self) -> None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    async def init(self) -> None:
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
            ) as cur:
                row = await cur.fetchone()
                return json.loads(row["data"]) if row else None

    async def delete(self, session_id: str) -> bool:
        async with aiosqlite.connect(DB_PATH) as db:
            cur = await db.execute(
                "DELETE FROM sessions WHERE session_id = ?", (session_id,)
            )
            await db.commit()
            return cur.rowcount > 0

    async def list_all(self, limit: int = 50) -> list[dict[str, Any]]:
        async with aiosqlite.connect(DB_PATH) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT data FROM sessions ORDER BY updated_at DESC LIMIT ?", (limit,)
            ) as cur:
                rows = await cur.fetchall()
        out = []
        for row in rows:
            s = json.loads(row["data"])
            out.append({
                "session_id": s["session_id"],
                "target_role": s.get("setup", {}).get("target_role", ""),
                "interview_type": s.get("setup", {}).get("interview_type", ""),
                "status": "completed" if s.get("interview_complete") else "active",
                "overall_score": s.get("overall_score", 0),
                "readiness": s.get("readiness_label", ""),
                "turn_count": len(s.get("evaluations", [])),
                "created_at": s.get("created_at"),
            })
        return out

    @staticmethod
    def new_id() -> str:
        return str(uuid.uuid4())
