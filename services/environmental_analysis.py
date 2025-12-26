import pandas as pd
from datetime import datetime, timedelta

def analyze_environmental_data(df):
    """Analyzes the previous day's environmental data and calculates a workability score."""
    
    # Get the previous day's date
    yesterday = (datetime.now() - timedelta(days=1)).date()
    
    # Convert Timestamp column to datetime type if not already
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    
    # Filter data for the previous day
    df_yesterday = df[df["Timestamp"].dt.date == yesterday]
    
    if df_yesterday.empty:
        return "No data available for the previous day."

    # optimal thresholds for a good working environment
    ideal_ranges = {
        "Temperature (°C)": (20, 25),
        "Humidity (%)": (40, 60),
        "CO₂ (ppm)": (400, 800),
        "PM2.5 (µg/m³)": (0, 35),
        "Noise Level (dB)": (35, 55),
        "Lighting (Lux)": (300, 700),
    }

    # Compute how many readings fall within the ideal range
    total_records = len(df_yesterday)
    score = 0

    for parameter, (low, high) in ideal_ranges.items():
        within_range = df_yesterday[parameter].between(low, high).sum()
        score += (within_range / total_records) * 100  # Normalize score for each parameter
    
    # Final workability score (average of all parameters)
    workability_score = round(score / len(ideal_ranges), 2)

    return {
        "Workability Score":workability_score/100,
        "Date": yesterday
    }

# Example usage with generated data
df = pd.read_csv('/Users/kdn_aigayatrikadam/Documents/Projects/Project-4/ESG Wellbeing Agent/backend/data_pipeline/environmental_data.csv') # Generate a week's data
print(analyze_environmental_data(df))