from pydantic import BaseModel, Field
from typing import Any, Optional, Dict, List
from datetime import datetime


class HealthOut(BaseModel):
    status: str = "ok"


class OfficerCreate(BaseModel):
    id: str
    name: str
    role: str = "officer"
    last_lat: Optional[float] = None
    last_lon: Optional[float] = None


class OfficerOut(BaseModel):
    id: str
    name: str
    role: str
    last_lat: Optional[float] = None
    last_lon: Optional[float] = None


class AlertCreate(BaseModel):
    type: str = Field(..., examples=["crowd_density"])
    priority: str = Field(..., examples=["P1", "P2", "P3", "P4"])
    lat: float
    lon: float
    confidence: float = Field(..., ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AlertOut(BaseModel):
    id: str
    type: str
    priority: str
    lat: float
    lon: float
    confidence: float
    status: str
    created_at: datetime
    assigned_officer_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AlertUpdate(BaseModel):
    status: str = Field(..., examples=["ack", "resolved"])


class PatrolStartIn(BaseModel):
    officer_id: str
    start_lat: Optional[float] = None
    start_lon: Optional[float] = None
    location_text: Optional[str] = None


class PatrolOut(BaseModel):
    id: str
    officer_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    location_text: Optional[str] = None
    summary: Optional[str] = None
    risk_score: Optional[float] = None


class PatrolEndIn(BaseModel):
    notes: Optional[str] = None


class PatrolSummaryOut(BaseModel):
    patrol_id: str
    summary: str
    risk_score: float
    generated_with: str
    rag_context_docs: List[str] = Field(default_factory=list)


class RagIngestIn(BaseModel):
    doc_id: str
    doc_type: str = "SOP"
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RagQueryIn(BaseModel):
    query: str
    k: int = 4
    filters: Dict[str, Any] = Field(default_factory=dict)


class RagQueryOut(BaseModel):
    query: str
    results: List[Dict[str, Any]]
