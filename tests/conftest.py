import server
import pytest
from flask import template_rendered


@pytest.fixture
def captured_templates(app=server.app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)
        
@pytest.fixture
def client():
    with server.app.test_client() as client:
        yield client

@pytest.fixture
def clubs():
    return [
        {
            "name": "Test club",
            "email": "test_club@test.com",
            "points": "10"
        },
        {
            "name": "Test other club",
            "email": "test_club@test.com",
            "points": "100"
        }

    ]

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
        },
        {
            "name": "Test competition",
            "date": "2023-12-10 08:55:23",
            "numberOfPlaces": "20",
            "investedPoints": {
                "Test club": {
                    "places": 1,
                    "points": 2
                }
            }
        }
    ]
