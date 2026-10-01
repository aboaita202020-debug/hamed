from fastapi.testclient import TestClient

from app.main import app


def test_runtime_endpoints():
    client = TestClient(app)
    assert client.get('/').status_code == 200
    assert client.get('/dashboard').status_code == 200
    assert client.get('/health').json()['status'] == 'ok'
    assert client.get('/readiness').json()['ready'] is True
    assert client.get('/status').status_code == 200
