from fastapi import APIRouter

from app.api.deps import DbSession
from app.schemas.session import CreateSessionResponse, SessionSummary
from app.services.practice_session_service import PracticeSessionService
from app.services.stats_service import StatsService

router = APIRouter()
practice_session_service = PracticeSessionService()
stats_service = StatsService()


@router.post("/sessions", response_model=CreateSessionResponse)
def create_session(db: DbSession) -> CreateSessionResponse:
    session_id = practice_session_service.create_session(db)
    return CreateSessionResponse(session_id=session_id)


@router.get("/sessions/{session_id}/summary", response_model=SessionSummary)
def get_session_summary(session_id: str, db: DbSession) -> SessionSummary:
    summary = stats_service.get_summary(session_id, db)
    return SessionSummary(**summary)
