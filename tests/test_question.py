from http import HTTPStatus


def test_create_question(client, user, subject, difficulty):
    response = client.post(
        '/questions/',
        json={
            'text': 'What is the capital of France?',
            'subject_id': subject.id,
            'difficulty_id': difficulty.id,
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
        'subject_id': subject.id,
        'difficulty_id': difficulty.id,
        'subject': {'id': subject.id, 'name': subject.name},
        'difficulty': {'id': difficulty.id, 'name': difficulty.name},
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


def test_get_by_id(client, question):
    response = client.get('/questions/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': question.id,
        'text': question.text,
        'subject_id': question.subject_id,
        'difficulty_id': question.difficulty_id,
        'subject': {'id': question.subject.id, 'name': question.subject.name},
        'difficulty': {
            'id': question.difficulty.id,
            'name': question.difficulty.name,
        },
        'options': [
            {
                'id': option.id,
                'description': option.description,
                'letter': option.letter,
                'is_correct': option.is_correct,
            }
            for option in question.options
        ],
    }


def test_get_by_invalid_id(client):
    response = client.get('/questions/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Question not found'}
