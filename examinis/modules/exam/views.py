from typing import List

from fastapi import APIRouter, Depends

from examinis.modules.exam.schemas import ExamSchema
from examinis.modules.exam.service import ExamService

router = APIRouter(
    prefix='/exam',
    tags=['exam'],
)


@router.get('/', response_model=List[ExamSchema])
def get_all(exam_service: ExamService = Depends(ExamService)):
    return exam_service.get_all()


@router.get('/{exam_id}', response_model=ExamSchema)
def get_by_id(exam_id: int, exam_service: ExamService = Depends(ExamService)):
    return exam_service.get(exam_id)
