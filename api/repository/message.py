import uuid
from sqlalchemy.orm import Session
from api.model.message import MessageModel
from api.entity.message import MessageEntity


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, messageEntity: MessageEntity) -> MessageEntity:
        message_model = MessageModel(
            message_id=str(uuid.uuid4()),
            name=messageEntity.name,
            content=messageEntity.content,
        )
        self.db.add(message_model)
        self.db.commit()
        self.db.refresh(message_model)
        return MessageEntity.from_model(message_model)

    def find_all(self) -> list[MessageEntity]:
        return [
            MessageEntity.from_model(message_model)
            for message_model in self.db.query(MessageModel).all()
        ]
