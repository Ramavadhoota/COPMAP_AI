import os
from datetime import datetime
from sqlalchemy.orm import Session

from app.config import settings
from app.db import SessionLocal, init_db
from app.models import Officer
from app.services.rag_service import rag_service


def upsert_officer(db: Session, officer: Officer):
    existing = db.get(Officer, officer.id)
    if existing:
        existing.name = officer.name
        existing.role = officer.role
        existing.last_lat = officer.last_lat
        existing.last_lon = officer.last_lon
        existing.last_seen_at = officer.last_seen_at
        db.add(existing)
    else:
        db.add(officer)
    db.commit()


def main():
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    init_db()

    db = SessionLocal()
    try:
        upsert_officer(db, Officer(
            id="officer_1",
            name="Officer A",
            role="field",
            last_lat=12.9716,
            last_lon=77.5946,
            last_seen_at=datetime.utcnow(),
        ))
        upsert_officer(db, Officer(
            id="officer_2",
            name="Officer B",
            role="field",
            last_lat=12.9750,
            last_lon=77.6000,
            last_seen_at=datetime.utcnow(),
        ))

        sop_path = os.path.join(settings.DATA_DIR, "samples", "sop.md")
        if os.path.exists(sop_path):
            with open(sop_path, "r", encoding="utf-8") as f:
                content = f.read()
            rag_service.ingest(
                doc_id="sop_nakabandi_1",
                content=content,
                metadata={"doc_type": "SOP", "topic": "nakabandi"},
            )
            print("Ingested SOP into Chroma:", "sop_nakabandi_1")
        else:
            print("No SOP found at:", sop_path)

        print("Seed complete.")
        print("Officers: officer_1, officer_2")
    finally:
        db.close()


if __name__ == "__main__":
    main()
