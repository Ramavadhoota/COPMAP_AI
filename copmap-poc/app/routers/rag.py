from fastapi import APIRouter
from ..schemas import RagQueryIn, RagQueryOut
from ..services.rag_service import rag_service

router = APIRouter(prefix="/api/v1/rag", tags=["rag"])


@router.post("/query", response_model=RagQueryOut)
def query(payload: RagQueryIn):
    hits = rag_service.query(query_text=payload.query, k=payload.k, where=payload.filters)
    return RagQueryOut(query=payload.query, results=hits)
