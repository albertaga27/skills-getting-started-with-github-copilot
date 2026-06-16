"""Shared pytest fixtures for testing the FastAPI application."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Provide a TestClient instance with a fresh copy of activities data.
    This fixture ensures test isolation by resetting the activities database
    before each test.
    """
    # Create a fresh copy of activities for this test
    test_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 3,  # Lower limit for testing capacity
            "participants": ["michael@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 2,  # Lower limit for testing capacity
            "participants": []
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 2,
            "participants": []
        }
    }
    
    # Replace app's activities with test data
    activities.clear()
    activities.update(test_activities)
    
    # Create and return the test client
    return TestClient(app)
