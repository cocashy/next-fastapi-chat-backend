from api.domain.entity.message import MessageEntity


class MessageReq:
    name: str
    content: str

    @classmethod
    def from_json(cls, json: dict):
        instance = cls()
        instance.name = json["name"]
        instance.content = json["content"]
        return instance

    def to_entity(self):
        return MessageEntity(
            name=self.name,
            content=self.content,
        )


class MessageRes:
    message_id: str
    name: str
    content: str
    created_at: str
    updated_at: str

    @classmethod
    def from_entity(cls, message):
        instance = cls()
        instance.message_id = message.message_id
        instance.name = message.name
        instance.content = message.content
        instance.created_at = message.created_at.isoformat()
        instance.updated_at = message.updated_at.isoformat()
        return instance

    def to_json(self):
        return {
            "message_id": self.message_id,
            "name": self.name,
            "content": self.content,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
