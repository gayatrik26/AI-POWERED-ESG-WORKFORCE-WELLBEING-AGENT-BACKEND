from fastapi import APIRouter, HTTPException
import json
import os
import pandas as pd
from services.productivity_analysis import calculate_productivity_score
router = APIRouter()

@router.get("/get_productivity_score")
def get_productivity_score():
    """API endpoint to return the productivity score."""
    df = pd.read_csv("/Users/kdn_aigayatrikadam/Documents/Projects/Project-4/ESG Wellbeing Agent/backend/data_pipeline/productivity_data.csv")
    result = calculate_productivity_score(df)
    return result