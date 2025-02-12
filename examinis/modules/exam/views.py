from typing import List

from fastapi import APIRouter, Depends

from examinis.common.schemas.pagination_schema import PageParams, PagedResponseSchema
from examinis.modules.exam.schemas import (
    ExamAutomaticCreationSchema,
    ExamListSchema,
    ExamManualCreationSchema,
    ExamPageParams,
    ExamSchema,
)
from examinis.modules.exam.service import ExamService

router = APIRouter(
    prefix='/exams',
    tags=['exams'],
)


@router.get('/', response_model=PagedResponseSchema[ExamListSchema])
def get_all(
    params: ExamPageParams = Depends(ExamPageParams),
    exam_service: ExamService = Depends(ExamService)):
    return exam_service.get_all_paginated(params)


@router.get('/{exam_id}', response_model=ExamSchema)
def get_by_id(exam_id: int, exam_service: ExamService = Depends(ExamService)):
    return exam_service.get(exam_id)


@router.post('/manual', response_model=ExamSchema)
def create_manual(
    exam: ExamManualCreationSchema,
    exam_service: ExamService = Depends(ExamService),
):
    return exam_service.create_manual(exam)


@router.post('/automatic', response_model=ExamSchema)
def create_automatic(
    exam: ExamAutomaticCreationSchema,
    exam_service: ExamService = Depends(ExamService),
):
    return exam_service.create_automatic(exam)
