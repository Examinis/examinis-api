import datetime
from contextlib import contextmanager

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from examinis.app import app
from examinis.db.config import get_session
from examinis.models.base import Base
from tests.factories import (
    DifficultyFactory,
    QuestionFactory,
    SubjectFactory,
    UserFactory,
)


@pytest.fixture(scope='session')
def engine():
    """Create a Postgres container and return an SQLAlchemy engine."""	
    with PostgresContainer('postgres:17.2', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture
def session(engine):
    """Create a new database session for a test."""
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    Base.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    """Create a FastAPI test client with a test database session."""	
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@contextmanager
def _mock_db_time(*, model, time=datetime.datetime(2025, 1, 1)):
    def fake_time_handler(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_handler)

    yield time

    event.remove(model, 'before_insert', fake_time_handler)


@pytest.fixture
def mock_db_time():
    """Mock the current time for a database model."""
    return _mock_db_time


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


@pytest.fixture
def question(session):
    question = QuestionFactory()

    session.add(question)
    session.commit()
    session.refresh(question)

    return question
