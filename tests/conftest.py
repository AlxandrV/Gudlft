import server
import pytest

@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client

@pytest.fixture
def clubs():
    return [{
        "name":"Test club",
        "email":"test_club@test.com",
        "points":"10"
    }]