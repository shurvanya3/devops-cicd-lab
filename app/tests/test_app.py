import pytest
from src.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Проверка эндпоинта /health"""
    rv = client.get('/health')
    assert rv.status_code == 200
    assert rv.get_json() == {"status": "ok"}

def test_index_endpoint_status(client):
    """Проверка доступности эндпоинта /"""
    rv = client.get('/')
    assert rv.status_code == 200

def test_index_endpoint_content(client):
    """Проверка структуры JSON на эндпоинте /"""
    rv = client.get('/')
    data = rv.get_json()
    assert "service" in data
    assert "version" in data
    assert "hostname" in data
