from http import HTTPStatus


def test_create_question(client):
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
        'text': 'What is the capital of France?',
        'subject_id': 1,
        'difficulty_id': 1,
        'options': [
            {'description': 'Paris', 'letter': 'A', 'is_correct': True},
            {'description': 'London', 'letter': 'B', 'is_correct': False},
            {'description': 'Berlin', 'letter': 'C', 'is_correct': False},
            {'description': 'Madrid', 'letter': 'D', 'is_correct': False},
        ],
    }
