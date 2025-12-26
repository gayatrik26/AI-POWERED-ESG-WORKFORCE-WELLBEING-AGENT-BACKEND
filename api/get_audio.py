import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

AUDIO_DIR = "/Users/kdn_aigayatrikadam/Documents/Projects/Project-4/ESG Wellbeing Agent/backend/data_pipeline/employee_audio"

@router.get("/audio/{employee_id}/{audio_name}")
async def get_employee_audio(employee_id: str, audio_name: str):
    audio_path = os.path.join(AUDIO_DIR, employee_id, f"{audio_name}.wav")
    
    if os.path.exists(audio_path):
        return FileResponse(audio_path)
    
    raise HTTPException(status_code=404, detail="Audio not found")
