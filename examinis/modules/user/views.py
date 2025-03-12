from typing import List

from fastapi import APIRouter, Depends

from examinis.modules.user.schemas import UserCreateSchema, UserSchema
from examinis.modules.user.service import UserService

router = APIRouter(
    prefix='/user',
    tags=['user'],
)


@router.get('/', response_model=List[UserSchema])
def get_all(user_service: UserService = Depends(UserService)):
    return user_service.get_all()


@router.get('/{user_id}', response_model=UserSchema)
def get_by_id(user_id: int, user_service: UserService = Depends(UserService)):
    return user_service.get(user_id)


@router.post('/', response_model=UserSchema)
def create(
    user: UserCreateSchema, user_service: UserService = Depends(UserService)
):
    return user_service.create(user)
