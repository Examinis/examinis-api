from fastapi import APIRouter, Depends

from examinis.modules.question.schemas import (
    QuestionCreateSchema,
    QuestionSchema,
)
from examinis.modules.question.service import QuestionService

router = APIRouter(
    prefix='/question',
    tags=['question'],
)


@router.get('/{question_id}', response_model=QuestionSchema)
def get_by_id(
        question_id: int,
        service: QuestionService = Depends(QuestionService)
):
    return service.get(question_id)


@router.post('/', response_model=QuestionCreateSchema)
def create(
        question: QuestionCreateSchema,
        service: QuestionService = Depends(QuestionService)
):
    return service.create(question)
