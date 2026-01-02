"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Sharpen your mind and compete in chess tournaments.",
        "schedule": "Wednesdays 3:30-5:00pm, Room 204",
        "max_participants": 20,
        "participants": ["michael@mergington.edu", "emma@mergington.edu"]
    },
    "Robotics Team": {
        "description": "Build and program robots for regional competitions.",
        "schedule": "Mondays & Thursdays 4:00-6:00pm, Lab 3",
        "max_participants": 15,
        "participants": ["anna@mergington.edu","david@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce school plays and musicals.",
        "schedule": "Tuesdays 3:30-5:30pm, Auditorium",
        "max_participants": 25,
        "participants": ["olivia@mergington.edu", "noah@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Compete in science events and experiments.",
        "schedule": "Fridays 3:30-5:00pm, Science Wing",
        "max_participants": 18,
        "participants": ["ava@mergington.edu", "william@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore your creativity with painting, drawing, and sculpture.",
        "schedule": "Thursdays 3:30-5:00pm, Art Room",
        "max_participants": 20,
        "participants": ["mia@mergington.edu", "james@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up for this activity")           
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
