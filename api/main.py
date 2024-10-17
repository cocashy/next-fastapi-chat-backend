from fastapi import FastAPI, WebSocket, Depends
from sqlalchemy.orm import Session
from api.database.config import get_db
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List
from api.domain.usecase.message import MessageUsecase
import logging
from api.schema.message import MessageReq, MessageRes
from api.domain.entity.message import MessageEntity

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://next-fastapi-chat-frontend.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: MessageEntity):
        for connection in self.active_connections:
            await connection.send_json(MessageRes.from_entity(message).to_json())


connection_manager = ConnectionManager()


@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await connection_manager.connect(websocket)

    message_usecase = MessageUsecase(db)
    messages = message_usecase.find_all()
    for message in messages:
        await websocket.send_json(MessageRes.from_entity(message).to_json())

    try:
        while True:
            json = await websocket.receive_json()
            message_req = MessageReq.from_json(json)
            message = message_usecase.create(message_req.to_entity())
            await connection_manager.broadcast(message)
    except Exception as e:
        logger.error(f"Error: {e}")
        connection_manager.disconnect(websocket)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
