from typing import List

from fastapi import APIRouter, Depends

from examinis.core.security import get_current_user
from examinis.modules.subject.schemas import SubjectSchema
from examinis.modules.subject.service import SubjectService

router = APIRouter(
    prefix='/subject',
    tags=['subject'],
    dependencies=[Depends(get_current_user)],
)


@router.get('/', response_model=List[SubjectSchema])
def get_all(subject_service: SubjectService = Depends(SubjectService)):
    return subject_service.get_all()


@router.get('/{subject_id}', response_model=SubjectSchema)
def get_by_id(
    subject_id: int, subject_service: SubjectService = Depends(SubjectService)
):
    return subject_service.get(subject_id)
