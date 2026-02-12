import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db import init_db
from .ws import manager

from .routers.health import router as health_router
from .routers.alerts import router as alerts_router
from .routers.patrols import router as patrols_router
from .routers.rag import router as rag_router
from .routers.documents import router as documents_router


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_list(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.on_event("startup")
    def _startup():
        os.makedirs(settings.DATA_DIR, exist_ok=True)
        init_db()

    # REST routers
    app.include_router(health_router)
    app.include_router(alerts_router)
    app.include_router(patrols_router)
    app.include_router(rag_router)
    app.include_router(documents_router)

    # WebSocket: officer live alerts
    @app.websocket("/ws/officers/{officer_id}")
    async def ws_officer(websocket: WebSocket, officer_id: str):
        await manager.connect(officer_id, websocket)
        try:
            while True:
                # keepalive / allow client pings
                await websocket.receive_text()
        except WebSocketDisconnect:
            manager.disconnect(officer_id)

    return app


app = create_app()
