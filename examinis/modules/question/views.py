from http import HTTPStatus

from fastapi import APIRouter, Depends

from examinis.common.schemas.pagination_schema import (PagedResponseSchema,
                                                       PageParams)
from examinis.modules.question.schemas import (QuestionBaseSchema,
                                               QuestionCreateSchema,
                                               QuestionSchema,
                                               QuestionUpdateSchema)
from examinis.modules.question.service import QuestionService

router = APIRouter(
    prefix='/questions',
    tags=['questions'],
)


@router.get('/', response_model=PagedResponseSchema[QuestionSchema])
def get_questions(
    params: PageParams = Depends(PageParams),
    service: QuestionService = Depends(QuestionService),
):
    return service.get_all_paginated(params)


@router.get('/{question_id}', response_model=QuestionSchema)
def get_by_id(
    question_id: int, service: QuestionService = Depends(QuestionService)
):
    return service.get(question_id)


@router.post(
    '/',
    response_model=QuestionSchema,
    status_code=HTTPStatus.CREATED,
)
def create(
    question: QuestionCreateSchema,
    service: QuestionService = Depends(QuestionService),
):
    return service.create(question)


@router.put('/{question_id}', response_model=QuestionBaseSchema)
def update(
    question_id: int,
    question: QuestionUpdateSchema,
    service: QuestionService = Depends(QuestionService),
):
    return service.update(question_id, question.model_dump())

@router.delete('/{question_id}', status_code=HTTPStatus.NO_CONTENT)
def delete(
    question_id: int,
    service: QuestionService = Depends(QuestionService),
):
    return service.delete(question_id)