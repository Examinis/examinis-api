from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash

from examinis.modules.auth.repository import AuthRepository

SECRET_KEY = '123'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 5000

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/')


def hash_password(password: str):
    """Hashes the password using the PasswordHash library"""
    return pwd_context.hash(password)


def verify_password(password: str, hash: str):
    """Verifies if the password matches the hash"""
    return pwd_context.verify(password, hash)


def create_access_token(data: dict):
    """Creates an access token"""
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_repository: AuthRepository = Depends(),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        subject_id = payload.get('sub')

        if not subject_id:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    user = auth_repository.get_by_email(subject_id)

    if not user:
        raise credentials_exception

    return user
