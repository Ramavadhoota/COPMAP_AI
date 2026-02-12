from fastapi import APIRouter
from ..schemas import RagIngestIn
from ..services.rag_service import rag_service

router = APIRouter(prefix="/api/v1/documents", tags=["documents"])


@router.post("/ingest")
def ingest(payload: RagIngestIn):
    meta = dict(payload.metadata or {})
    meta["doc_type"] = payload.doc_type
    rag_service.ingest(doc_id=payload.doc_id, content=payload.content, metadata=meta)
    return {"status": "ingested", "doc_id": payload.doc_id}
