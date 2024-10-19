import os
import logging
from typing import List
from dotenv import load_dotenv

import uvicorn
from fastapi import Depends, FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from api.db.config import get_db
from api.entity.message import MessageEntity
from api.usecase.message import MessageUsecase
from api.schema.message import MessageReq

load_dotenv()

# ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv("APP_URL"),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    def __init__(self):
        self.active_sockets: List[WebSocket] = []

    async def connect(self, socket: WebSocket):
        await socket.accept()
        self.active_sockets.append(socket)

    def disconnect(self, socket: WebSocket):
        self.active_sockets.remove(socket)

    async def broadcast(self, message: MessageEntity):
        res = message.to_schema()
        json_ = res.model_dump()
        for socket in self.active_sockets:
            await socket.send_json(json_)


connection_manager = ConnectionManager()


@app.websocket("/chat")
async def websocket_endpoint(socket: WebSocket, db: Session = Depends(get_db)):
    await connection_manager.connect(socket)

    message_usecase = MessageUsecase(db)
    message_models = message_usecase.find_all()
    for model in message_models:
        entity = MessageEntity.from_model(model)
        json_ = entity.to_schema().model_dump()
        await socket.send_json(json_)

    try:
        while True:
            json_ = await socket.receive_json()
            req = MessageReq(**json_)
            entity = MessageEntity.from_schema(req)
            entity = message_usecase.create(entity)
            await connection_manager.broadcast(entity)
    except Exception as e:
        logger.error(f"Error: {e}")
        connection_manager.disconnect(socket)


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
