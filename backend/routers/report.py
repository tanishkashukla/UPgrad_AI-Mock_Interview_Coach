from fastapi import APIRouter, HTTPException

from backend.services.orchestrator import Orchestrator

router = APIRouter(tags=["report"])
orch = Orchestrator()


@router.get("/session/{session_id}/report")
async def get_report(session_id: str):
    try:
        return await orch.generate_report(session_id)
    except ValueError as e:
        raise HTTPException(404, str(e)) from e
    except Exception as e:
        raise HTTPException(500, str(e)) from e
