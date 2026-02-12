from datetime import datetime
from sqlalchemy import String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base


class Officer(Base):
    __tablename__ = "officers"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    role: Mapped[str] = mapped_column(String(50), default="officer")

    last_lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    last_lon: Mapped[float | None] = mapped_column(Float, nullable=True)
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    alerts: Mapped[list["Alert"]] = relationship(back_populates="assigned_officer")


class Patrol(Base):
    __tablename__ = "patrols"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    officer_id: Mapped[str] = mapped_column(String(64), ForeignKey("officers.id"))

    start_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    start_lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    start_lon: Mapped[float | None] = mapped_column(Float, nullable=True)

    location_text: Mapped[str | None] = mapped_column(String(200), nullable=True)

    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    risk_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    incidents: Mapped[list["Incident"]] = relationship(back_populates="patrol")


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    type: Mapped[str] = mapped_column(String(60))
    priority: Mapped[str] = mapped_column(String(10))  # P1..P4
    lat: Mapped[float] = mapped_column(Float)
    lon: Mapped[float] = mapped_column(Float)
    confidence: Mapped[float] = mapped_column(Float)

    status: Mapped[str] = mapped_column(String(20), default="open")  # open|ack|resolved
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    assigned_officer_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("officers.id"), nullable=True)
    assigned_officer: Mapped[Officer | None] = relationship(back_populates="alerts")

    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    incidents: Mapped[list["Incident"]] = relationship(back_populates="alert")


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    patrol_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("patrols.id"), nullable=True)
    alert_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("alerts.id"), nullable=True)

    type: Mapped[str] = mapped_column(String(60))
    description: Mapped[str] = mapped_column(Text)

    lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    lon: Mapped[float | None] = mapped_column(Float, nullable=True)

    ts: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    evidence_urls_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    patrol: Mapped[Patrol | None] = relationship(back_populates="incidents")
    alert: Mapped[Alert | None] = relationship(back_populates="incidents")
