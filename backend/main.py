"""InterviewPilot AI — FastAPI entry point."""
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db.database import SessionDatabase
from backend.routers import interview, report, session

db = SessionDatabase()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init()
    yield


app = FastAPI(
    title="InterviewPilot AI",
    description="Production-grade multi-agent mock interview coach",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session.router)
app.include_router(interview.router)
app.include_router(report.router)


@app.get("/health")
async def health():
    from backend.utils.llm_client import LLMClient
    llm = LLMClient()
    return {
        "status": "ok",
        "service": "InterviewPilot AI",
        "mock_mode": llm.mock,
    }


@app.get("/sessions")
async def list_sessions():
    from backend.services.orchestrator import Orchestrator
    return await Orchestrator().list_sessions()
