from sqlalchemy.orm import Session
from api.database.model.message import MessageModel
from api.domain.entity.message import MessageEntity
import uuid


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
        return message_model.to_entity()

    def find_all(self) -> list[MessageEntity]:
        return [
            message_model.to_entity()
            for message_model in self.db.query(MessageModel).all()
        ]
