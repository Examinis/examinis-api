from http import HTTPStatus

from fastapi import Depends, HTTPException

from examinis.core.security import hash_password
from examinis.core.service_abstract import ServiceAbstract
from examinis.models.user import User
from examinis.modules.role.role_enum import RoleEnum
from examinis.modules.user.repository import UserRepository
from examinis.modules.user.schemas import UserCreateSchema
from examinis.modules.user_status.user_status_enum import UserStatusEnum


class UserService(ServiceAbstract[User]):
    def __init__(
        self,
        repository: UserRepository = Depends(UserRepository),
    ):
        super().__init__(repository)
        self.repository = repository

    def create(self, user: UserCreateSchema):
        if self.repository.get_by_email(user.email):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='User with this email already exists',
            )

        user_dict = user.model_dump()
        user_dict['password'] = hash_password(user_dict['password'])
        user_dict['role_id'] = RoleEnum.PROFESSOR.value
        user_dict['status_id'] = UserStatusEnum.PENDING.value

        return super().create(user_dict)
