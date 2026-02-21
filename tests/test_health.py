import pytest
from src.bot.web import app

def test_health_check():
    with app.test_client() as client:
        response = client.get('/health')
        assert response.status_code == 200
        assert response.data.decode('utf-8') == "OK"

def test_index_check():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
        assert "Weather Bot is running" in response.data.decode('utf-8')
