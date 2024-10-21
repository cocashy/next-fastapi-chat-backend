from typing import List
from fastapi import APIRouter, Depends, WebSocket

from sqlalchemy.orm import Session

from api.db.config import get_db
from api.entity.message import MessageEntity
from api.usecase.message import MessageUsecase
from api.schema.message import MessageReq

router = APIRouter()


class ChatConnectionManager:
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


connection_manager = ChatConnectionManager()


@router.get("/messages")
async def get_messages(db: Session = Depends(get_db)):
    message_usecase = MessageUsecase(db)
    message_models = message_usecase.find_all()
    return [message.to_schema().model_dump() for message in message_models]


@router.post("/messages")
async def post_messages(req: MessageReq, db: Session = Depends(get_db)):
    message_usecase = MessageUsecase(db)
    entity = MessageEntity.from_schema(req)
    entity = message_usecase.create(entity)
    return entity.to_schema().model_dump()


@router.websocket("/messages/broadcast")
async def websocket_endpoint(socket: WebSocket):
    await connection_manager.connect(socket)

    try:
        while True:
            json_ = await socket.receive_json()
            req = MessageReq(**json_)
            entity = MessageEntity.from_schema(req)
            await connection_manager.broadcast(entity)
    except Exception as e:
        connection_manager.disconnect(socket)
        raise e


@router.get("/sockets")
async def get_sockets():
    return [str(socket.client) for socket in connection_manager.active_sockets]
