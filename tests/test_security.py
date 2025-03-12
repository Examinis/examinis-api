from http import HTTPStatus
from examinis.core.security import ALGORITHM, SECRET_KEY, create_access_token

from jwt import decode

def test_jwt():
    data = {'sub': 'test@test.com'}

    token = create_access_token(data)
    
    result = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert result['sub'] == data['sub']
    assert result['exp']
    

def test_get_token(client, user):
    response = client.post(
        '/auth',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token