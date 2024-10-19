from dataclasses import dataclass
from datetime import datetime
from api.model.message import MessageModel
from api.schema.message import MessageReq, MessageRes


@dataclass
class MessageEntity:
    name: str
    content: str
    message_id: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_model(cls, model: MessageModel):
        return cls(
            name=model.name,
            content=model.content,
            message_id=model.message_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def to_model(self) -> MessageModel:
        return MessageModel(
            message_id=self.message_id,
            name=self.name,
            content=self.content,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_schema(req: MessageReq, message_id: str = ""):
        return MessageEntity(
            name=req.name,
            content=req.content,
            message_id=message_id,  # IDは後から設定する場合
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

    def to_schema(self) -> MessageRes:
        return MessageRes(
            message_id=self.message_id,
            name=self.name,
            content=self.content,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat(),
        )
