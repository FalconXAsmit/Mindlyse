from pydantic import BaseModel
from typing import Optional

class Message(BaseModel):
    timestamp: Optional[str] = None
    speaker: str
    text: str

class Conversation(BaseModel):
    filename: str
    message_count: int
    messages: list[Message]