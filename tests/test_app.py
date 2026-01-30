import pytest
from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


def test_root():
    """Test that root endpoint redirects to index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities():
    """Test that activities endpoint returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert activities["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"


def test_get_activity_details():
    """Test that we can get details of a specific activity"""
    response = client.get("/activities")
    activities = response.json()
    chess_club = activities["Chess Club"]
    assert "participants" in chess_club
    assert "michael@mergington.edu" in chess_club["participants"]
    assert chess_club["max_participants"] == 12


def test_signup_for_activity():
    """Test successful signup for an activity"""
    response = client.post(
        "/activities/Chess%20Club/signup?email=test@example.com",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]
    assert "test@example.com" in result["message"]


def test_signup_duplicate_student():
    """Test that duplicate signup returns 400 error"""
    # Try to sign up a student who is already registered
    response = client.post(
        "/activities/Chess%20Club/signup?email=michael@mergington.edu",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_invalid_activity():
    """Test signup for non-existent activity returns 404"""
    response = client.post(
        "/activities/Invalid%20Activity/signup?email=test@example.com",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_participant():
    """Test unregistering a participant from an activity"""
    # First, sign up a new participant
    client.post(
        "/activities/Drama%20Club/signup?email=newtestuser@example.com",
        headers={"Content-Type": "application/json"}
    )
    
    # Then unregister them
    response = client.post(
        "/unregister",
        json={
            "email": "newtestuser@example.com",
            "activity": "Drama Club"
        }
    )
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]


def test_unregister_invalid_participant():
    """Test unregistering a non-existent participant returns 404"""
    response = client.post(
        "/unregister",
        json={
            "email": "nonexistent@example.com",
            "activity": "Chess Club"
        }
    )
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_unregister_invalid_activity():
    """Test unregistering from non-existent activity returns 404"""
    response = client.post(
        "/unregister",
        json={
            "email": "michael@mergington.edu",
            "activity": "Invalid Activity"
        }
    )
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
