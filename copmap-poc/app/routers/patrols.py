from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Patrol
from ..schemas import PatrolStartIn, PatrolOut, PatrolEndIn, PatrolSummaryOut
from ..services.patrol_service import start_patrol, end_patrol_and_summarize
from ..services.rag_service import rag_service
from ..config import settings

router = APIRouter(prefix="/api/v1/patrols", tags=["patrols"])


@router.post("/start", response_model=PatrolOut)
def start(payload: PatrolStartIn, db: Session = Depends(get_db)):
    row = start_patrol(db, payload.officer_id, payload.start_lat, payload.start_lon, payload.location_text)
    return PatrolOut(
        id=row.id, officer_id=row.officer_id, start_time=row.start_time,
        end_time=row.end_time, location_text=row.location_text,
        summary=row.summary, risk_score=row.risk_score
    )


@router.post("/{patrol_id}/end", response_model=PatrolOut)
async def end(patrol_id: str, payload: PatrolEndIn, db: Session = Depends(get_db)):
    try:
        row = await end_patrol_and_summarize(db, patrol_id, payload.notes)
    except ValueError:
        raise HTTPException(status_code=404, detail="Patrol not found")
    return PatrolOut(
        id=row.id, officer_id=row.officer_id, start_time=row.start_time,
        end_time=row.end_time, location_text=row.location_text,
        summary=row.summary, risk_score=row.risk_score
    )


@router.get("/{patrol_id}/summary", response_model=PatrolSummaryOut)
def summary(patrol_id: str, db: Session = Depends(get_db)):
    patrol = db.get(Patrol, patrol_id)
    if not patrol:
        raise HTTPException(status_code=404, detail="Patrol not found")
    if not patrol.summary:
        raise HTTPException(status_code=400, detail="Summary not generated yet")

    query_text = patrol.location_text or "patrol"
    rag_hits = rag_service.query(query_text=query_text, k=3)
    rag_docs = [h["content"] for h in rag_hits]

    return PatrolSummaryOut(
        patrol_id=patrol.id,
        summary=patrol.summary,
        risk_score=float(patrol.risk_score or 0.0),
        generated_with=settings.LLM_MODE.lower(),
        rag_context_docs=rag_docs,
    )
