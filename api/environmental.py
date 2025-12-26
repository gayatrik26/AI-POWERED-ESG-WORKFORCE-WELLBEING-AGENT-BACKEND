from fastapi import APIRouter, HTTPException
import json
import os
import pandas as pd
from services.environmental_analysis import analyze_environmental_data
router = APIRouter()

@router.get("/get_workability_score")
def get_workability_score():
    """API endpoint to return the environmental workability score."""
    df = pd.read_csv('/Users/kdn_aigayatrikadam/Documents/Projects/Project-4/ESG Wellbeing Agent/backend/data_pipeline/environmental_data.csv') # Generate a week's data
    result = analyze_environmental_data(df)
    return result