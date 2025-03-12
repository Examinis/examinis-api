from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from examinis.core.security import create_access_token, verify_password
from examinis.core.service_abstract import ServiceAbstract
from examinis.models.user import User
from examinis.modules.auth.repository import AuthRepository


class AuthService(ServiceAbstract[User]):
    def __init__(
        self,
        repository: AuthRepository = Depends(),
    ):
        super().__init__(repository)
        self.repository = repository

    def login(self, form_data: OAuth2PasswordRequestForm) -> User:
        user = self.repository.get_by_email(form_data.username)

        if not user:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Incorrect email or password',
            )

        if not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail='Incorrect email or password',
            )

        access_token = create_access_token(data={'sub': user.email})

        return {'access_token': access_token, 'token_type': 'bearer'}
