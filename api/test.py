from fastapi import APIRouter, HTTPException
import json
import os
import pandas as pd
from services.cv_emotion import analyze_employee_images
router = APIRouter()

@router.get("/images-test-emotion")
def get_image_emotion(employee_id: str):
    result = analyze_employee_images(employee_id)
    return result
