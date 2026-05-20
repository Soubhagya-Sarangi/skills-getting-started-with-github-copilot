import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test"""
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Join the school soccer team for practice and matches",
            "schedule": "Tuesdays, Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["alex@mergington.edu", "nina@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Swim laps, work on technique, and prepare for swim meets",
            "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["liam@mergington.edu", "mia@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed media art projects",
            "schedule": "Mondays, 4:00 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["sophia@mergington.edu", "julia@mergington.edu"]
        },
        "Drama Club": {
            "description": "Practice acting, stagecraft, and prepare performances",
            "schedule": "Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["ethan@mergington.edu", "grace@mergington.edu"]
        },
        "Science Club": {
            "description": "Investigate science experiments and research projects",
            "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["noah@mergington.edu", "chloe@mergington.edu"]
        },
        "Debate Team": {
            "description": "Prepare arguments and compete in debate tournaments",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["olivia@mergington.edu", "mason@mergington.edu"]
        }
    }
    
    # Clear and reset activities
    activities.clear()
    activities.update(original_activities)
    yield
    # Cleanup after test
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def client():
    """Return TestClient for the FastAPI app"""
    return TestClient(app)
