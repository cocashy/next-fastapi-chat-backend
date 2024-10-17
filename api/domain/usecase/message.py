from api.database.repository.message import MessageRepository
from api.domain.entity.message import MessageEntity
from sqlalchemy.orm import Session


class MessageUsecase:
    def __init__(self, db: Session):
        self.message_repository = MessageRepository(db)

    def create(self, message: MessageEntity) -> MessageEntity:
        return self.message_repository.create(message)

    def find_all(self) -> list[MessageEntity]:
        return self.message_repository.find_all()
