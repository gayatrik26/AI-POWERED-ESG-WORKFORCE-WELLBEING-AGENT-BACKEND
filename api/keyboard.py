from fastapi import APIRouter, HTTPException
import json
import os
import pandas as pd
from services.behavioural_analysis import calculate_dominant_keyboard_emotion
router = APIRouter()

@router.get("/get_dominant_keyboard_emotion")
def get_keyboard_score():
    """API endpoint to return the keyboard emotions."""
    df = pd.read_excel("/Users/kdn_aigayatrikadam/Documents/Projects/Project-4/ESG Wellbeing Agent/backend/data_pipeline/keyboard_employee.xlsx")
    result = calculate_dominant_keyboard_emotion(df)
    return result