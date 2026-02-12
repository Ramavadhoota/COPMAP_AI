# app/routers/alerts.py

import json
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Alert
from ..schemas import AlertCreate, AlertOut, AlertUpdate
from ..services.alert_service import create_alert_and_notify

router = APIRouter(prefix="/api/v1/alerts", tags=["alerts"])


@router.post("", response_model=AlertOut)
async def create_alert(payload: AlertCreate, db: Session = Depends(get_db)):
    alert_id = f"alert_{uuid.uuid4().hex[:10]}"

    row = await create_alert_and_notify(
        db=db,
        alert_id=alert_id,
        type_=payload.type,
        priority=payload.priority,
        lat=payload.lat,
        lon=payload.lon,
        confidence=payload.confidence,
        metadata=payload.metadata,
    )

    return AlertOut(
        id=row.id,
        type=row.type,
        priority=row.priority,
        lat=row.lat,
        lon=row.lon,
        confidence=row.confidence,
        status=row.status,
        created_at=row.created_at,
        assigned_officer_id=row.assigned_officer_id,
        metadata=json.loads(row.metadata_json or "{}"),
    )


@router.get("", response_model=list[AlertOut])
def list_alerts(
    status: str | None = None,
    priority: str | None = None,
    assigned_officer_id: str | None = None,
    limit: int = 200,
    db: Session = Depends(get_db),
):
    q = db.query(Alert)

    if status:
        q = q.filter(Alert.status == status)
    if priority:
        q = q.filter(Alert.priority == priority)
    if assigned_officer_id:
        q = q.filter(Alert.assigned_officer_id == assigned_officer_id)

    rows = q.order_by(Alert.created_at.desc()).limit(min(max(limit, 1), 500)).all()

    out: list[AlertOut] = []
    for r in rows:
        out.append(
            AlertOut(
                id=r.id,
                type=r.type,
                priority=r.priority,
                lat=r.lat,
                lon=r.lon,
                confidence=r.confidence,
                status=r.status,
                created_at=r.created_at,
                assigned_officer_id=r.assigned_officer_id,
                metadata=json.loads(r.metadata_json or "{}"),
            )
        )
    return out


@router.patch("/{alert_id}", response_model=AlertOut)
def update_alert(alert_id: str, payload: AlertUpdate, db: Session = Depends(get_db)):
    row = db.get(Alert, alert_id)
    if not row:
        raise HTTPException(status_code=404, detail="Alert not found")

    # Basic state update (open -> ack -> resolved)
    row.status = payload.status
    if payload.status == "resolved":
        row.resolved_at = datetime.utcnow()

    db.add(row)
    db.commit()
    db.refresh(row)

    return AlertOut(
        id=row.id,
        type=row.type,
        priority=row.priority,
        lat=row.lat,
        lon=row.lon,
        confidence=row.confidence,
        status=row.status,
        created_at=row.created_at,
        assigned_officer_id=row.assigned_officer_id,
        metadata=json.loads(row.metadata_json or "{}"),
    )
