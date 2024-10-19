from datetime import datetime
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from api.db.config import engine

Base = declarative_base()


class MessageModel(Base):
    __tablename__ = "messages"

    message_id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    content = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.now, index=True)
    updated_at = Column(DateTime(timezone=True), default=datetime.now, index=True)


Base.metadata.create_all(bind=engine)
