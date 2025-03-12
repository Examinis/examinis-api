from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from examinis.modules.auth.schemas import TokenSchema
from examinis.modules.auth.service import AuthService

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/', response_model=TokenSchema)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(),
):
    return auth_service.login(form_data)
