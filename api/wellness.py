from fastapi import APIRouter, HTTPException
from services.llm import generate_wellness_program
from services.cv_emotion import analyze_employee_images
import os
import json

router = APIRouter()

@router.get("/wellness/{employee_id}")
def get_wellness_program(employee_id: str):
    """
    Fetches AI-generated wellness recommendations based on an employee's burnout score.
    Also saves detected emotions in the JSON.
    """
    DATA_FILE = "data_pipeline/synthetic_employees.json"
    
    if not os.path.exists(DATA_FILE):
        raise HTTPException(status_code=404, detail="Employee data file not found.")
    
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    
    employee = next((emp for emp in data if emp["id"] == employee_id), None)
    
    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee ID {employee_id} not found")

    emp_info = employee

    # Detect emotions via DeepFace
    emotions = analyze_employee_images(employee_id)
    if 'error' not in emotions:
        employee["image_detected_emotions"] = emotions
    else:
        print(f"Emotion detection error for {employee_id}: {emotions['error']}")
        employee["image_detected_emotions"] = {}

    # Generate wellness recommendation using LLM
    # ai_recommendation = generate_wellness_program(emp_info, employee_id)
    # employee["wellness_recommendation"] = ai_recommendation

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return {
        # "wellness_recommendation": ai_recommendation,
        "image_detected_emotions": emotions
    }