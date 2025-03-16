from http import HTTPStatus

from fastapi import Depends, HTTPException

from examinis.core.service_abstract import ServiceAbstract
from examinis.models.user_status import UserStatus
from examinis.modules.user_status.repository import UserStatusRepository


class UserStatusService(ServiceAbstract[UserStatus]):
    def __init__(
        self, repository: UserStatusRepository = Depends(UserStatusRepository)
    ):
        super().__init__(repository)

    def get(self, id: int) -> UserStatus:
        user_status = self.repository.get(id)

        if not user_status:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail='UserStatus not found',
            )

        return user_status
