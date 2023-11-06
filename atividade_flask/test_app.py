import pytest
from app import app as flask_app
import jwt
import datetime

class TestConfig:
    SECRET_KEY = 'afonsinho'

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

class TestAuthentication:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.secret_key = TestConfig.SECRET_KEY

    def create_token(self, exp):
        return jwt.encode({'exp': exp}, self.secret_key, algorithm='HS256')

    def test_create_message_without_token(self, client):
        response = client.post('/messages')
        assert response.status_code == 401
        assert b"Token is missing" in response.data

    def test_create_message_with_expired_token(self, client):
        expired_token = self.create_token(datetime.datetime.utcnow() - datetime.timedelta(seconds=1))
        headers = {'Authorization': f'Bearer {expired_token}'}
        response = client.post('/messages', headers=headers)
        assert response.status_code == 401
        assert b"Token expired" in response.data

    def test_create_message_with_valid_token(self, client):
        valid_token = self.create_token(datetime.datetime.utcnow() + datetime.timedelta(hours=1))
        headers = {'Authorization': f'Bearer {valid_token}'}
        response = client.post('/messages', headers=headers, json={"text": "Hello, World!"})
        assert response.status
