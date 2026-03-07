import os
os.environ['TESTING'] ="true";
import pytest
from app import create_app
from app.config import TestingConfig
from app.extensions import db



@pytest.fixture
def app():
    app = create_app(TestingConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    with app.test_client() as client :
        yield client

