import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from examinis.app import app
from examinis.models.base import Base


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:17.2', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@pytest.fixture(scope='function')
def session(engine: Engine):
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)
