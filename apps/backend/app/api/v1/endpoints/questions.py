from fastapi import APIRouter, Query

from app.schemas.question import QuestionResponse
from app.services.question_service import QuestionService

router = APIRouter()
service = QuestionService()


@router.get("/questions", response_model=QuestionResponse)
def get_question(
    module: str = Query(..., pattern="^(integer-operations|algebra-expressions|algebra-formulas)$"),
    difficulty: str = Query(..., pattern="^(easy|medium|hard)$"),
) -> QuestionResponse:
    return service.generate(module=module, difficulty=difficulty)
