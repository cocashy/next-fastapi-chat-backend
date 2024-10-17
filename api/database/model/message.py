from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from api.database.config import engine
from api.domain.entity.message import MessageEntity

Base = declarative_base()


# メッセージ履歴を保存するテーブル定義
class MessageModel(Base):
    __tablename__ = "messages"

    message_id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    content = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now, index=True)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, index=True)

    # session_id = Column(Integer, ForeignKey("Sessions.session_id"), index=True)
    # session = relationship("Session", back_populates="messages")
    # room_id = Column(Integer, index=True)
    # room = relationship("Room", foreign_keys="Room.room_id", back_populates="messages")

    # @classmethod
    # def from_entity(cls, message: MessageEntity):
    #     instance = cls()
    #     instance.message_id = message.message_id
    #     instance.name = message.name
    #     instance.content = message.content
    #     instance.created_at = message.created_at
    #     instance.updated_at = message.updated_at
    #     return instance

    def to_entity(self) -> MessageEntity:
        return MessageEntity(
            message_id=self.message_id,
            name=self.name,
            content=self.content,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


# テーブルを作成
Base.metadata.create_all(bind=engine)
