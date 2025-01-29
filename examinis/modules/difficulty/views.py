from typing import List

from fastapi import APIRouter, Depends

from examinis.modules.difficulty.schemas import DifficultySchema
from examinis.modules.difficulty.service import DifficultyService

router = APIRouter(
    prefix='/difficulty',
    tags=['difficulty'],
)


@router.get('/', response_model=List[DifficultySchema])
def get_all(
    difficulty_service: DifficultyService = Depends(DifficultyService),
):
    return difficulty_service.get_all()


@router.get('/{difficulty_id}', response_model=DifficultySchema)
def get_by_id(
    difficulty_id: int,
    difficulty_service: DifficultyService = Depends(DifficultyService),
):
    return difficulty_service.get(difficulty_id)
