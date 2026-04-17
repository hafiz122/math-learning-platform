from app.schemas.question import QuestionResponse
from app.services.generators.registry import generate_question


class QuestionService:
    def generate(self, module: str, difficulty: str) -> QuestionResponse:
        return generate_question(module, difficulty)
