from pydantic import BaseModel


class MessageReq(BaseModel):
    name: str
    content: str


class MessageRes(BaseModel):
    message_id: str
    name: str
    content: str
    created_at: str
    updated_at: str
