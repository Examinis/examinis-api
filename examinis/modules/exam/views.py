from fastapi import APIRouter, Depends

from examinis.common.schemas.pagination_schema import PagedResponseSchema
from examinis.core.security import get_current_user
from examinis.modules.exam.schemas import (
    ExamAutomaticCreationSchema,
    ExamCorrectionInputSchema,
    ExamCorrectionSchema,
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
    exam_service: ExamService = Depends(ExamService),
):
    return exam_service.get_all_paginated(params)


@router.get('/{exam_id}', response_model=ExamSchema)
def get_by_id(
    exam_id: int,
    exam_service: ExamService = Depends(ExamService),
):
    return exam_service.get(exam_id)


@router.post('/manual', response_model=ExamSchema)
def create_manual(
    exam: ExamManualCreationSchema,
    exam_service: ExamService = Depends(ExamService),
    user=Depends(get_current_user),
):
    return exam_service.create_manual(exam, user.id)


@router.post('/automatic', response_model=ExamSchema)
def create_automatic(
    exam: ExamAutomaticCreationSchema,
    exam_service: ExamService = Depends(ExamService),
    user=Depends(get_current_user),
):
    return exam_service.create_automatic(exam, user.id)


@router.post('/{exam_id}/grade', response_model=ExamCorrectionSchema)
def grade_exam(
    exam_id: int,
    answers: ExamCorrectionInputSchema,
    exam_service: ExamService = Depends(ExamService),
):
    return exam_service.grade(exam_id, answers.model_dump())
