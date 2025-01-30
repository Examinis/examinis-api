from http import HTTPStatus


def test_create_question(client, user, subject, difficulty):
    response = client.post(
        '/questions/',
        json={
            'text': 'What is the capital of France?',
            'subject_id': 1,
            'difficulty_id': 1,
            'options': [
                {'description': 'Paris', 'letter': 'A', 'is_correct': True},
                {'description': 'London', 'letter': 'B', 'is_correct': False},
                {'description': 'Berlin', 'letter': 'C', 'is_correct': False},
                {'description': 'Madrid', 'letter': 'D', 'is_correct': False},
            ],
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'text': 'What is the capital of France?',
        'subject_id': 1,
        'difficulty_id': 1,
        'subject': {'id': 1, 'name': 'Geography'},
        'difficulty': {'id': 1, 'name': 'Easy'},
        'options': [
            {
                'id': 1,
                'description': 'Paris',
                'letter': 'A',
                'is_correct': True,
            },
            {
                'id': 2,
                'description': 'London',
                'letter': 'B',
                'is_correct': False,
            },
            {
                'id': 3,
                'description': 'Berlin',
                'letter': 'C',
                'is_correct': False,
            },
            {
                'id': 4,
                'description': 'Madrid',
                'letter': 'D',
                'is_correct': False,
            },
        ],
    }


# def test_get_by_id(client):
#     response = client.get('/questions/1')

#     assert response.status_code == HTTPStatus.OK
#     assert response.json() == {
#         'id': 1,
#         'text': 'What is the capital of France?',
#         'subject_id': 1,
#         'difficulty_id': 1,
#         'options': [
#             {
#                 'id': 1,
#                 'description': 'Paris',
#                 'letter': 'A',
#                 'is_correct': True,
#             },
#             {
#                 'id': 2,
#                 'description': 'London',
#                 'letter': 'B',
#                 'is_correct': False,
#             },
#             {
#                 'id': 3,
#                 'description': 'Berlin',
#                 'letter': 'C',
#                 'is_correct': False,
#             },
#             {
#                 'id': 4,
#                 'description': 'Madrid',
#                 'letter': 'D',
#                 'is_correct': False,
#             },
#         ],
#     }


def test_get_by_invalid_id(client):
    response = client.get('/questions/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Question not found'}
