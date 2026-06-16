"""Happy path tests for the Activities API endpoints."""

import pytest


def test_get_activities(client):
    """Test retrieving all activities returns correct structure and data."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Verify all test activities are present
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Gym Class" in activities
    
    # Verify activity structure
    chess_club = activities["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_signup_success(client):
    """Test a student can successfully sign up for an activity."""
    response = client.post(
        "/activities/Programming%20Class/signup",
        params={"email": "john@mergington.edu"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "john@mergington.edu" in data["message"]
    
    # Verify student is now in participants
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "john@mergington.edu" in activities["Programming Class"]["participants"]


def test_signup_duplicate_prevented(client):
    """Test that a student cannot sign up for the same activity twice."""
    email = "duplicate@mergington.edu"
    activity = "Programming Class"
    
    # First signup should succeed
    response1 = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Second signup with same email should fail
    response2 = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    assert response2.status_code == 400
    data = response2.json()
    assert "already signed up" in data["detail"].lower()


def test_activity_capacity_enforced(client):
    """Test that students cannot sign up for activities that are at capacity."""
    activity = "Chess Club"  # Max 3 participants, already has michael@mergington.edu
    
    # Sign up first student (should succeed - 2/3 capacity)
    response1 = client.post(
        f"/activities/{activity}/signup",
        params={"email": "student1@mergington.edu"}
    )
    assert response1.status_code == 200
    
    # Sign up second student (should succeed - 3/3 capacity)
    response2 = client.post(
        f"/activities/{activity}/signup",
        params={"email": "student2@mergington.edu"}
    )
    assert response2.status_code == 200
    
    # Third student should fail - activity is now full
    response3 = client.post(
        f"/activities/{activity}/signup",
        params={"email": "student3@mergington.edu"}
    )
    assert response3.status_code == 400
    data = response3.json()
    assert "full" in data["detail"].lower()


def test_unregister_success(client):
    """Test a student can successfully unregister from an activity."""
    activity = "Chess Club"
    email = "michael@mergington.edu"
    
    # Verify student is initially registered
    activities_response = client.get("/activities")
    assert email in activities_response.json()[activity]["participants"]
    
    # Unregister the student
    response = client.post(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    assert response.status_code == 200
    data = response.json()
    assert "unregistered" in data["message"].lower()
    
    # Verify student is no longer registered
    activities_response = client.get("/activities")
    assert email not in activities_response.json()[activity]["participants"]
