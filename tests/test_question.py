from http import HTTPStatus
from unittest.mock import patch

from examinis.models.option import Option
from examinis.models.question import Question


def test_create_question(client, user, subject, difficulty, mock_db_time):
    payload = {
        'text': 'What is the capital of France?',
        'subject_id': subject.id,
        'difficulty_id': difficulty.id,
        'options': [
            {
                'description': 'Paris',
                'letter': 'A',
                'is_correct': True,
            },
            {
                'description': 'London',
                'letter': 'B',
                'is_correct': False,
            },
            {
                'description': 'Berlin',
                'letter': 'C',
                'is_correct': False,
            },
            {
                'description': 'Madrid',
                'letter': 'D',
                'is_correct': False,
            },
        ],
    }
    with mock_db_time(model=Question), mock_db_time(model=Option):
        response = client.post('/questions/', json=payload)

    assert response.status_code == HTTPStatus.CREATED

    response_data = response.json()
    assert response_data['text'] == 'What is the capital of France?'
    assert response_data['subject'] == {'id': subject.id, 'name': subject.name}
    assert response_data['difficulty'] == {
        'id': difficulty.id,
        'name': difficulty.name,
    }
    assert response_data['user'] == {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    assert response_data['created_at'] == '2025-01-01T00:00:00'

    expected_options = [
        {'description': 'Paris', 'letter': 'A', 'is_correct': True},
        {'description': 'London', 'letter': 'B', 'is_correct': False},
        {'description': 'Berlin', 'letter': 'C', 'is_correct': False},
        {'description': 'Madrid', 'letter': 'D', 'is_correct': False},
    ]

    response_options = [
        {
            'description': opt['description'],
            'letter': opt['letter'],
            'is_correct': opt['is_correct'],
        }
        for opt in response_data['options']
    ]

    assert response_options == expected_options


def test_get_by_id(client, question):
    response = client.get(f'/questions/{question.id}')

    assert response.status_code == HTTPStatus.OK

    response_data = response.json()

    assert response_data['id'] == question.id
    assert response_data['text'] == question.text
    assert response_data['user'] == {
        'id': question.user.id,
        'first_name': question.user.first_name,
        'last_name': question.user.last_name,
    }
    assert response_data['subject'] == {
        'id': question.subject.id,
        'name': question.subject.name,
    }
    assert response_data['difficulty'] == {
        'id': question.difficulty.id,
        'name': question.difficulty.name,
    }

    expected_options = [
        {
            'id': option.id,
            'description': option.description,
            'letter': option.letter,
            'is_correct': option.is_correct,
        }
        for option in question.options
    ]

    response_options = response_data['options']

    assert response_options == expected_options


def test_get_by_invalid_id(client):
    response = client.get('/questions/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Question not found'}


def test_delete_question(client, question, session):
    response = client.delete(f'/questions/{question.id}')

    assert response.status_code == HTTPStatus.NO_CONTENT

    deleted_question = session.get(Question, question.id)
    assert deleted_question is None


def test_delete_question_with_image(client, question, session):
    img_path = '/fake/path/to/image.jpg'
    question.image_path = img_path
    session.commit()

    with patch('os.remove') as mock_remove:
        response = client.delete(f'/questions/{question.id}')

        assert response.status_code == HTTPStatus.NO_CONTENT

        mock_remove.assert_called_once_with(img_path)

        deleted_question = session.get(Question, question.id)
        assert deleted_question is None


def test_delete_question_image_not_found(client, question, session):
    img_path = '/fake/path/to/image.jpg'
    question.image_path = img_path
    session.commit()

    with patch('os.remove', side_effect=FileNotFoundError) as mock_remove:
        response = client.delete(f'/questions/{question.id}')

        assert response.status_code == HTTPStatus.NO_CONTENT

        mock_remove.assert_called_once_with(img_path)

        deleted_question = session.get(Question, question.id)
        assert deleted_question is None


def test_update_question(client, question, session):
    payload = {
        'id': question.id,
        'text': 'Updated Question?',
        'subject_id': question.subject.id,
        'difficulty_id': question.difficulty.id,
        'options': [
            {'description': 'Option 1', 'letter': 'A', 'is_correct': False},
            {'description': 'Option 2', 'letter': 'B', 'is_correct': True},
            {'description': 'Option 3', 'letter': 'C', 'is_correct': False},
            {'description': 'Option 4', 'letter': 'D', 'is_correct': False},
        ],
    }

    response = client.put('/questions/', json=payload)

    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data['id'] == question.id
    assert data['text'] == 'Updated Question?'
    assert len(data['options']) == 4

    session.refresh(question)
    assert question.text == 'Updated Question?'
    assert len(question.options) == 4
