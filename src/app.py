# Unregister a participant from an activity (must be after app and activities are defined)


from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path
from src.activities_data import activities

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


def get_activities_store():
    from src.activities_data import activities
    return activities


@app.get("/activities")
def get_activities(store=Depends(get_activities_store)):
    return store


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, store=Depends(get_activities_store)):
    """Sign up a student for an activity"""
    if activity_name not in store:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = store[activity_name]
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, store=Depends(get_activities_store)):
    """Unregister a student from an activity"""
    if activity_name not in store:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity = store[activity_name]
    if email not in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student not registered for this activity")
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
