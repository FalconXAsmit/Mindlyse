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


class FlaggedMessage(BaseModel):
    message_index: int
    speaker: str
    tactic: str
    explanation: str


class AnalysisResult(BaseModel):
    flagged_messages: list[FlaggedMessage]
    pattern_summary: str
    severity: str
    dominant_tactic: str
