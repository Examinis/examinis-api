from http import HTTPStatus

from fastapi import APIRouter, Depends, UploadFile

from examinis.common.schemas.pagination_schema import (
    PagedResponseSchema,
    PageParams,
)
from examinis.modules.question.schemas import (
    QuestionCreateSchema,
    QuestionListSchema,
    QuestionPageParams,
    QuestionSchema,
    QuestionUpdateSchema,
)
from examinis.modules.question.service import QuestionService

router = APIRouter(
    prefix='/questions',
    tags=['questions'],
)


@router.get('/', response_model=PagedResponseSchema[QuestionListSchema])
def get_questions(
    params: QuestionPageParams = Depends(QuestionPageParams),
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


@router.put('/', response_model=QuestionSchema)
def update(
    question: QuestionUpdateSchema,
    service: QuestionService = Depends(QuestionService),
):
    return service.update(question)


@router.delete('/{question_id}', status_code=HTTPStatus.NO_CONTENT)
def delete(
    question_id: int,
    service: QuestionService = Depends(QuestionService),
):
    return service.delete(question_id)


@router.post('/upload-image', status_code=HTTPStatus.OK)
async def upload_image(
    id: int,
    image: UploadFile,
    service: QuestionService = Depends(QuestionService),
):
    return await service.upload_image(id, image)


@router.get('/{question_id}/image', status_code=HTTPStatus.OK)
def get_question_image(
    question_id: int,
    service: QuestionService = Depends(QuestionService),
):
    return service.get_image(question_id)
