import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_home(client):
    res = client.get('/')
    assert res.status_code == 200
    assert res.json == {"message": "Welcome to the Flask App!"}

def test_add(client):
    res = client.get('/add?a=5&b=7')
    assert res.status_code == 200
    assert res.json == {"result": 12}

def test_greet(client):
    res = client.get('/greet/ayush')
    assert res.status_code == 200
    assert res.json == {"message": "Hello, ayush!"}

def test_is_even(client):
    res = client.get('/iseven/4')
    assert res.status_code == 200
    assert res.json == {"number": 4, "is_even": True}

    res = client.get('/iseven/3')
    assert res.status_code == 200
    assert res.json == {"number": 3, "is_even": False}