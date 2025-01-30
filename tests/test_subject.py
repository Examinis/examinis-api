from http import HTTPStatus

def test_get_subject(client, subject):
    response = client.get(f"/subject/{subject.id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": subject.id,
        "name": subject.name,
    }

def test_get_subject_not_found(client):
    response = client.get("/subject/999")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Subject not found"}