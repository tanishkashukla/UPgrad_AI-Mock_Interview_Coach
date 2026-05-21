from fastapi import APIRouter, HTTPException

from backend.services.orchestrator import Orchestrator
from backend.state.models import SessionStartRequest

router = APIRouter(prefix="/session", tags=["session"])
orch = Orchestrator()


@router.post("/start")
async def start_session(body: SessionStartRequest):
    try:
        setup = {
            "target_role": body.target_role,
            "background": body.background,
            "interview_type": body.interview_type.value,
            "experience_level": body.experience_level.value,
        }
        return await orch.start_session(setup)
    except Exception as e:
        raise HTTPException(500, str(e)) from e


@router.get("/{session_id}/history")
async def session_history(session_id: str):
    try:
        return await orch.get_history(session_id)
    except ValueError as e:
        raise HTTPException(404, str(e)) from e


@router.delete("/{session_id}")
async def delete_session(session_id: str):
    ok = await orch.delete_session(session_id)
    if not ok:
        raise HTTPException(404, "Session not found")
    return {"deleted": True}
