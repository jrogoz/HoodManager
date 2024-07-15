import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import scoped_session, sessionmaker

from sql_app.models import models
from sql_app.main import get_db, app


@pytest.fixture(scope='session')
def db_engine():
    url_object = URL.create(
        "postgresql",
        username='postgres',
        password='12345',
        host='localhost',
        database='HM_test',
        port=5432
    )

    engine = create_engine(url_object)
    models.Base.metadata.create_all(bind=engine)
    yield engine
    models.Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope='session')
def db_session_factory(db_engine):
    return scoped_session(sessionmaker(bind=db_engine))


@pytest.fixture(scope='function')
def db_session(db_session_factory):
    session = db_session_factory()
    yield session
    try:
        session.query(models.Sim).delete()
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()


@pytest.fixture(scope='function')
def override_get_db(db_session):
    def _override_get_db():
        try:
            yield db_session
        finally:
            pass
    return _override_get_db


@pytest.fixture(scope='function')
def client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides = {}

