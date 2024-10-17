from datetime import datetime


class MessageEntity:
    def __init__(
        self,
        name: str,
        content: str,
        message_id: str = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        self.message_id = message_id
        self.name = name
        self.content = content
        self.created_at = created_at
        self.updated_at = updated_at
