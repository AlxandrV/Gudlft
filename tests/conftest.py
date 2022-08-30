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

@pytest.fixture
def competitions():
    return [
        {
            "name": "Test competition",
            "date": "2022-12-10 08:55:23",
            "numberOfPlaces": "20"
        },
                {
            "name": "Test competition in past",
            "date": "2020-12-10 08:55:23",
            "numberOfPlaces": "10"
        }
    ]