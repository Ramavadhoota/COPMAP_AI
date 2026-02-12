import json
import math
from datetime import datetime
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from ..models import Alert, Officer
from ..ws import manager


def _haversine_km(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    lat1, lon1 = a
    lat2, lon2 = b
    r = 6371.0
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    x = math.sin(dlat / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlon / 2) ** 2
    return 2 * r * math.asin(math.sqrt(x))


def assign_officer(db: Session, lat: float, lon: float, max_km: float = 5.0) -> Optional[str]:
    officers = db.query(Officer).all()
    best_id = None
    best_dist = 1e9

    for o in officers:
        if o.last_lat is None or o.last_lon is None:
            continue
        dist = _haversine_km((lat, lon), (o.last_lat, o.last_lon))
        if dist < best_dist and dist <= max_km:
            best_dist = dist
            best_id = o.id

    return best_id


async def create_alert_and_notify(
    db: Session,
    alert_id: str,
    type_: str,
    priority: str,
    lat: float,
    lon: float,
    confidence: float,
    metadata: dict,
) -> Alert:
    assigned = assign_officer(db, lat, lon)

    row = Alert(
        id=alert_id,
        type=type_,
        priority=priority,
        lat=lat,
        lon=lon,
        confidence=confidence,
        status="open",
        created_at=datetime.utcnow(),
        assigned_officer_id=assigned,
        metadata_json=json.dumps(metadata or {}, ensure_ascii=False),
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    payload = {
        "event": "alert_created",
        "alert": {
            "id": row.id,
            "type": row.type,
            "priority": row.priority,
            "lat": row.lat,
            "lon": row.lon,
            "confidence": row.confidence,
            "status": row.status,
            "created_at": row.created_at.isoformat(),
            "assigned_officer_id": row.assigned_officer_id,
            "metadata": metadata or {},
        },
    }

    if assigned:
        await manager.send_to_officer(assigned, payload)

    return row
