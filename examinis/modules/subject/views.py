from typing import List
from fastapi import APIRouter, Depends

from examinis.modules.subject.schemas import SubjectSchema
from examinis.modules.subject.service import SubjectService


router = APIRouter(
    prefix='/subject',
    tags=['subject'],
)

@router.get('/', response_model=List[SubjectSchema])
def get_all(subject_service: SubjectService = Depends(SubjectService)):
    return subject_service.get_all()


@router.get('/{role_id}', response_model=SubjectSchema)
def get_by_id(role_id: int, subject_service: SubjectService = Depends(SubjectService)):
    return subject_service.get(role_id)

