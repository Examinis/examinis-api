from typing import List

from fastapi import APIRouter, Depends

from examinis.core.security import get_current_user
from examinis.modules.user.schemas import UserCreateSchema, UserSchema
from examinis.modules.user.service import UserService

router = APIRouter(
    prefix='/user',
    tags=['user'],
)


@router.get('/', response_model=List[UserSchema], dependencies=[Depends(get_current_user)])
def get_all(user_service: UserService = Depends(UserService)):
    return user_service.get_all()


@router.get('/{user_id}', response_model=UserSchema, dependencies=[Depends(get_current_user)])
def get_by_id(user_id: int, user_service: UserService = Depends(UserService)):
    return user_service.get(user_id)


@router.post('/', response_model=UserSchema)
def create(
    user: UserCreateSchema, user_service: UserService = Depends(UserService)
):
    return user_service.create(user)
