import os
os.environ['TESTING'] ="true";
import pytest
from app import create_app
from app.config import TestingConfig
from app.extensions import db
from tests.factories import UserFactory



@pytest.fixture(scope="session")
def app():
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope="function")
def client(app):
    with app.test_client() as client :
        yield client


@pytest.fixture(scope="function")
def db_session(app):
    with app.app_context():
        yield db.session
        db.session.rollback()
        db.session.remove()

@pytest.fixture()
def user_factory(db_session):
    UserFactory._meta.sqlalchemy_session = db_session
    return UserFactory