import pytest
import os
from app import app, db, Counter

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            counter = Counter.query.first()
            if counter is None:
                counter = Counter(value=0)
                db.session.add(counter)
                db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

def test_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Docker is Awesome!' in response.data

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.data == b'Healthy'

def test_readiness_check(client):
    response = client.get('/ready')
    assert response.status_code in [200, 503]

def test_docker_logo(client):
    response = client.get('/logo')
    assert response.status_code == 200
    assert response.mimetype == 'image/png'

def test_external_call(client, monkeypatch):
    def mock_get(url):
        class MockResponse:
            def __init__(self, text, status_code):
                self.text = text
                self.status_code = status_code
        return MockResponse("Mocked external call response", 200)

    monkeypatch.setattr('requests.get', mock_get)
    os.environ['EXTERNAL_ENDPOINT'] = 'http://example.com'
    response = client.get('/external-call')
    assert response.status_code == 200
    assert b'External call response: Mocked external call response' in response.data
