"""
Tests for the Mergington High School Activities API
"""
import pytest
from fastapi.testclient import TestClient


class TestGetActivities:
    """Tests for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        
        activities = response.json()
        assert isinstance(activities, dict)
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Gym Class" in activities
    
    def test_get_activities_returns_correct_structure(self, client):
        """Test that each activity has required fields"""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)
    
    def test_get_activities_includes_existing_participants(self, client):
        """Test that activities include existing participants"""
        response = client.get("/activities")
        activities = response.json()
        
        chess_club = activities["Chess Club"]
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]


class TestRootEndpoint:
    """Tests for GET / endpoint"""
    
    def test_root_redirects_to_index(self, client):
        """Test that root endpoint redirects to /static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_new_participant_success(self, client):
        """Test successful signup of a new participant"""
        response = client.post(
            "/activities/Chess Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]
    
    def test_signup_duplicate_participant_fails(self, client):
        """Test that signing up the same participant twice returns 400 error"""
        # First signup
        response1 = client.post(
            "/activities/Chess Club/signup?email=duplicate@mergington.edu"
        )
        assert response1.status_code == 200
        
        # Second signup with same email
        response2 = client.post(
            "/activities/Chess Club/signup?email=duplicate@mergington.edu"
        )
        assert response2.status_code == 400
        data = response2.json()
        assert "already signed up" in data["detail"]
    
    def test_signup_already_registered_participant_fails(self, client):
        """Test that signing up an already registered participant fails"""
        response = client.post(
            "/activities/Chess Club/signup?email=michael@mergington.edu"
        )
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]
    
    def test_signup_to_nonexistent_activity_fails(self, client):
        """Test that signing up for non-existent activity returns 404 error"""
        response = client.post(
            "/activities/Nonexistent Activity/signup?email=student@mergington.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]
    
    def test_signup_multiple_participants_to_same_activity(self, client):
        """Test adding multiple different participants to same activity"""
        email1 = "participant1@mergington.edu"
        email2 = "participant2@mergington.edu"
        
        response1 = client.post(f"/activities/Chess Club/signup?email={email1}")
        assert response1.status_code == 200
        
        response2 = client.post(f"/activities/Chess Club/signup?email={email2}")
        assert response2.status_code == 200
        
        # Verify both were added
        activities_response = client.get("/activities")
        activities = activities_response.json()
        participants = activities["Chess Club"]["participants"]
        assert email1 in participants
        assert email2 in participants
    
    def test_signup_different_activities(self, client):
        """Test same participant can sign up for different activities"""
        email = "multi@mergington.edu"
        
        response1 = client.post(f"/activities/Chess Club/signup?email={email}")
        assert response1.status_code == 200
        
        response2 = client.post(f"/activities/Programming Class/signup?email={email}")
        assert response2.status_code == 200
        
        # Verify participant in both activities
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities["Chess Club"]["participants"]
        assert email in activities["Programming Class"]["participants"]


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/signup/{email} endpoint"""
    
    def test_unregister_existing_participant_success(self, client):
        """Test successful removal of existing participant"""
        response = client.delete(
            "/activities/Chess Club/signup/michael@mergington.edu"
        )
        assert response.status_code == 200
        data = response.json()
        assert "Removed" in data["message"]
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    
    def test_unregister_nonexistent_participant_fails(self, client):
        """Test removing non-existent participant returns 404 error"""
        response = client.delete(
            "/activities/Chess Club/signup/nonexistent@mergington.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Participant not found" in data["detail"]
    
    def test_unregister_from_nonexistent_activity_fails(self, client):
        """Test removing from non-existent activity returns 404 error"""
        response = client.delete(
            "/activities/Nonexistent Activity/signup/student@mergington.edu"
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]
    
    def test_unregister_then_signup_again(self, client):
        """Test that participant can sign up again after unregistering"""
        email = "reregister@mergington.edu"
        activity = "Chess Club"
        
        # Sign up
        response1 = client.post(f"/activities/{activity}/signup?email={email}")
        assert response1.status_code == 200
        
        # Unregister
        response2 = client.delete(f"/activities/{activity}/signup/{email}")
        assert response2.status_code == 200
        
        # Sign up again
        response3 = client.post(f"/activities/{activity}/signup?email={email}")
        assert response3.status_code == 200
        
        # Verify participant is registered
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity]["participants"]
    
    def test_unregister_multiple_times(self, client):
        """Test that only one removal succeeds for a participant"""
        email = "michael@mergington.edu"
        activity = "Chess Club"
        
        # First removal succeeds
        response1 = client.delete(f"/activities/{activity}/signup/{email}")
        assert response1.status_code == 200
        
        # Second removal fails
        response2 = client.delete(f"/activities/{activity}/signup/{email}")
        assert response2.status_code == 404
