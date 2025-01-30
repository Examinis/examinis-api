import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from examinis.app import app
from examinis.db.config import get_session
from examinis.models.base import Base
from tests.factories import DifficultyFactory, SubjectFactory, UserFactory


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:17.2', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session(engine):
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    Base.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    user = UserFactory()

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def subject(session):
    subject = SubjectFactory()

    session.add(subject)
    session.commit()
    session.refresh(subject)

    return subject


@pytest.fixture
def difficulty(session):
    difficulty = DifficultyFactory()

    session.add(difficulty)
    session.commit()
    session.refresh(difficulty)

    return difficulty
