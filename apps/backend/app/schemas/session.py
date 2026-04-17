from app.schemas.common import BaseSchema


class CreateSessionResponse(BaseSchema):
    session_id: str


class SessionSummary(BaseSchema):
    session_id: str
    attempts: int
    correct_attempts: int
    accuracy: float
