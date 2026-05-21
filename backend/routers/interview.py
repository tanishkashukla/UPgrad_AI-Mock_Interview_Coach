from fastapi import APIRouter, HTTPException

from backend.services.orchestrator import Orchestrator
from backend.state.models import TurnRequest

router = APIRouter(tags=["interview"])
orch = Orchestrator()


@router.post("/session/{session_id}/turn")
async def submit_turn(session_id: str, body: TurnRequest):
    try:
        return await orch.process_turn(session_id, body.answer)
    except ValueError as e:
        raise HTTPException(404, str(e)) from e
    except Exception as e:
        raise HTTPException(500, str(e)) from e
