from typing import Dict
from fastapi import WebSocket
from fastapi.websockets import WebSocketState


class ConnectionManager:
    def __init__(self):
        self.active: Dict[str, WebSocket] = {}

    async def connect(self, officer_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active[officer_id] = websocket

    def disconnect(self, officer_id: str):
        self.active.pop(officer_id, None)

    async def send_to_officer(self, officer_id: str, payload: dict):
        ws = self.active.get(officer_id)
        if not ws:
            return
        if ws.application_state != WebSocketState.CONNECTED:
            return
        await ws.send_json(payload)


manager = ConnectionManager()
