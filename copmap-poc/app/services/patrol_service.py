import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Patrol, Alert
from .rag_service import rag_service
from .llm_service import llm_service


def start_patrol(db: Session, officer_id: str, start_lat: float | None, start_lon: float | None, location_text: str | None) -> Patrol:
    pid = f"patrol_{uuid.uuid4().hex[:10]}"
    row = Patrol(
        id=pid,
        officer_id=officer_id,
        start_time=datetime.utcnow(),
        start_lat=start_lat,
        start_lon=start_lon,
        location_text=location_text,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


async def end_patrol_and_summarize(db: Session, patrol_id: str, notes: str | None) -> Patrol:
    patrol = db.get(Patrol, patrol_id)
    if not patrol:
        raise ValueError("Patrol not found")

    patrol.end_time = datetime.utcnow()

    # For PoC: pull alerts assigned to this officer during patrol window
    q = db.query(Alert).filter(Alert.assigned_officer_id == patrol.officer_id)
    if patrol.start_time:
        q = q.filter(Alert.created_at >= patrol.start_time)
    if patrol.end_time:
        q = q.filter(Alert.created_at <= patrol.end_time)
    alerts = q.order_by(Alert.created_at.desc()).all()

    alerts_payload = []
    for a in alerts:
        alerts_payload.append({
            "id": a.id,
            "type": a.type,
            "priority": a.priority,
            "status": a.status,
            "lat": a.lat,
            "lon": a.lon,
            "confidence": a.confidence,
        })

    query_text = patrol.location_text or notes or "patrol summary"
    rag_hits = rag_service.query(query_text=query_text, k=4)
    rag_context = [h["content"] for h in rag_hits]

    llm_out = await llm_service.generate_patrol_summary(
        patrol={
            "id": patrol.id,
            "officer_id": patrol.officer_id,
            "start_time": patrol.start_time.isoformat(),
            "end_time": patrol.end_time.isoformat() if patrol.end_time else None,
            "location_text": patrol.location_text,
        },
        alerts=alerts_payload,
        notes=notes,
        rag_context=rag_context,
    )

    # store
    patrol.summary = llm_out["text"]
    # reuse llm risk heuristic for now
    patrol.risk_score = llm_service._risk_score(alerts_payload)  # type: ignore

    db.add(patrol)
    db.commit()
    db.refresh(patrol)
    return patrol
