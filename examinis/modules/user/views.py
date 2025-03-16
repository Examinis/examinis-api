from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import EmailStr

from examinis.core.security import get_current_user
from examinis.modules.user.schemas import UserCreateSchema, UserSchema
from examinis.modules.user.service import UserService

router = APIRouter(
    prefix='/user',
    tags=['user'],
)


@router.get(
    '/',
    response_model=List[UserSchema],
    dependencies=[Depends(get_current_user)],
)
def get_all(user_service: UserService = Depends(UserService)):
    return user_service.get_all()


@router.get(
    '/{user_id}',
    response_model=UserSchema,
    dependencies=[Depends(get_current_user)],
)
def get_by_id(user_id: int, user_service: UserService = Depends(UserService)):
    return user_service.get(user_id)


# @router.post('/', response_model=UserSchema)
# def create(
#     user: UserCreateSchema,
#     user_service: UserService = Depends(UserService)
# ):
#     return user_service.create(user)


# @router.post('/{user_id}/identity_proof', response_model=UserSchema)
# async def upload_identity_proof(
#     user_id: int,
#     identity_proof: UploadFile = File(...),
#     user_service: UserService = Depends(UserService)
# ):
#     return await user_service.upload_identity_proof(user_id, identity_proof)


@router.post('/', response_model=UserSchema)
async def create(
    first_name: str = Form(..., min_length=2, max_length=50),
    last_name: str = Form(..., min_length=2, max_length=50),
    email: EmailStr = Form(...),
    password: str = Form(..., min_length=8),
    institution: Optional[str] = Form(None),
    identity_proof: UploadFile = File(...),
    user_service: UserService = Depends(UserService),
):
    user = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'institution': institution,
    }
    return await user_service.create(user, identity_proof)
