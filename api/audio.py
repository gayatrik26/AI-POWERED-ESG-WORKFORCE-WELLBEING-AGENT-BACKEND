from fastapi import APIRouter, HTTPException
from services.audio_analysis import predict_emotion_from_audio
import os
import json

router = APIRouter()

# Define the root directory where employee audio files are stored
EMPLOYEE_AUDIO_ROOT = "/Users/kdn_aigayatrikadam/Documents/Projects/Project-4/ESG Wellbeing Agent/backend/data_pipeline/employee_audio"  # Change this to the correct path

@router.get("/predict-emotion/{employee_id}")
async def predict(employee_id: str):
    try:
        # Construct the path to the employee's folder
        employee_folder = os.path.join(EMPLOYEE_AUDIO_ROOT, employee_id)

        if not os.path.exists(employee_folder):
            raise HTTPException(status_code=404, detail="Employee ID not found")

        # Search for an audio file in the employee's folder
        audio_file = None
        for root, _, files in os.walk(employee_folder):
            for file in files:
                if file.endswith(".wav"):  # Adjust based on expected file format
                    audio_file = os.path.join(root, file)
                    break  # Stop searching after finding the first audio file
            if audio_file:
                break

        if not audio_file:
            raise HTTPException(status_code=404, detail="No audio file found for employee")

        # Process the audio file to predict emotion
        result = predict_emotion_from_audio(audio_file)

        DATA_FILE = os.path.join(os.path.dirname(__file__), "../data_pipeline/synthetic_employees.json")

        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        for e in data:
            if e["id"] == employee_id:
                e["audio_analysis_emotion"] = result
                break

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
            print("[INFO] JSON file updated successfully.")

        return {"employee_id": employee_id, "emotion": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
