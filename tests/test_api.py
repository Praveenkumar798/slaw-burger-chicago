import pytest
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_dashboard_access(client):
    """Test that the main dashboard loads."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Slawburger" in response.data

def test_api_stock(client):
    """Test the stock API endpoint."""
    response = client.get('/api/stock')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_api_history(client):
    """Test the history API endpoint."""
    response = client.get('/api/history')
    assert response.status_code == 200
    assert "deliveries" in response.json
    assert "waste" in response.json

def test_api_menu_local(client):
    """Test the local menu API endpoint."""
    response = client.get('/api/menu/local')
    assert response.status_code == 200
    assert response.json["status"] == "success"
