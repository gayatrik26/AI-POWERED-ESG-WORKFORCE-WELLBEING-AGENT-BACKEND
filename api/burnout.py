from fastapi import APIRouter, HTTPException
from services.burnout_calculator import calculate_burnout
from services.sentiment_analysis import analyze_sentiment
import json
import os
import pandas as pd
import numpy as np

router = APIRouter()

DATA_FILE = "data_pipeline/synthetic_employees.json"

def categorize_sentiment_label(score):
    """
    Categorizes the sentiment score into labels based on the range -1 to 1.
    """
    if -1 <= score < -0.5:
        return "very negative"
    elif -0.5 <= score < 0:
        return "negative"
    elif 0 <= score < 0.4:
        return "neutral"
    elif 0.4 <= score < 0.8:
        return "positive"
    elif 0.8 <= score <= 1:
        return "very positive"
    else:
        return "unknown"  
    

def calculate_stress_score(data, employee_id):
    """
    Calculate stress score for a given employee based on various health metrics.

    Parameters:
    data (DataFrame): Wearable dataset containing health metrics.
    employee_id (str): Unique ID of the employee.

    Returns:
    float: Stress Score (0-100)
    """

    user_data = data[data["User_ID"] == employee_id]
    
    if user_data.empty:
        return f"Employee ID {employee_id} not found in the dataset."
    
    # Normalize relevant features to a 0-100 scale
    sleep_quality = np.interp(user_data["Sleep_Duration"].values[0], [4, 10], [0, 100])
    deep_sleep_bonus = np.interp(user_data["Deep_Sleep_Duration"].values[0], [0.5, user_data["Sleep_Duration"].values[0]], [0, -20])  # More deep sleep reduces stress
    wakeup_penalty = np.interp(user_data["Wakeups"].values[0], [0, 5], [100, 0])  # More wakeups = worse sleep
    
    # Heart Rate penalty (both high & low HR are bad)
    hr = user_data["Heart_Rate"].values[0]
    if hr < 60:
        heart_rate_penalty = np.interp(hr, [50, 60], [100, 0])  # Too low is bad
    elif hr > 100:
        heart_rate_penalty = np.interp(hr, [100, 180], [0, 100])  # Too high is bad
    else:
        heart_rate_penalty = 0  # Normal range
    
    # Blood oxygen level is good for stress (higher is better)
    blood_oxygen_bonus = np.interp(user_data["Blood_Oxygen_Level"].values[0], [90, 100], [20, 0])  # Higher oxygen = lower stress
    
    # Hydration helps reduce stress
    hydration_bonus = np.interp(user_data["Water_Intake"].values[0], [0.5, 5], [20, 0])  # More hydration = lower stress
    
    # Caloric balance (bad diet increases stress)
    calorie_balance_penalty = np.interp(user_data["Calories_Intake"].values[0], [500, 5000], [100, 0])  
    
    # Mood & Lifestyle factors
    mood_score = {"Happy": 0, "Neutral": 25, "Sad": 75, "Anxious": 100}[user_data["Mood"].values[0]]
    stress_level_score = {"Low": 0, "Moderate": 50, "High": 100}[user_data["Stress_Level"].values[0]]
    smoking_penalty = 100 if user_data["Smoker"].values[0] == "Yes" else 0
    alcohol_penalty = {"No": 10, "Moderate": 50, "Heavy": 100}[user_data["Alcohol_Consumption"].values[0]]
    
    # Aggregate scores with weights
    stress_score = (
        (sleep_quality * 0.15) +
        (deep_sleep_bonus * 0.10) +  
        (wakeup_penalty * 0.10) +
        (heart_rate_penalty * 0.15) +
        (blood_oxygen_bonus * -0.10) +  
        (hydration_bonus * -0.10) +  
        (calorie_balance_penalty * 0.10) +
        (mood_score * 0.10) +
        (stress_level_score * 0.10) +
        (smoking_penalty * 0.05) +
        (alcohol_penalty * 0.05)
    )
    
    return max(0, round(stress_score, 2))  


@router.get("/burnout/{employee_id}")
def get_burnout_score(employee_id: str):
    """Calculate burnout score including email & feedback sentiment analysis."""
    
    if not os.path.exists(DATA_FILE):
        raise HTTPException(status_code=404, detail="Employee data not found.")
    
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    
    employee = next((emp for emp in data if emp["id"] == employee_id), None)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")

    
    # working_hours = employee.get("working_hours", 8)
    # meeting_overload = sum(employee.get("meeting_overload", {}).values())  

    
    email_bodies = [email["body"] for email in employee.get("emails", [])]
    email_sentiments = []
    email_sentiment_label = []

    for email in email_bodies:
        sentiment_result = analyze_sentiment(email)
        if isinstance(sentiment_result, dict) and 'score' in sentiment_result and 'label' in sentiment_result:
            email_sentiments.append(sentiment_result['score'])
            email_sentiment_label.append(sentiment_result['label'])
        else:
            email_sentiments.append(0.5)  
            email_sentiment_label.append("neutral")

    email_sentiment_score = round(sum(email_sentiments) / len(email_sentiments), 2) if email_sentiments else 0.5

    past_feedback_text = employee.get("hr_feedback", "").strip()

    print(f"DEBUG: Employee {employee_id}")  

    if past_feedback_text:
        feedback_sentiment_result = analyze_sentiment(past_feedback_text)
        print(f"DEBUG: Employee {employee_id} - Feedback Sentiment Result: {feedback_sentiment_result}") 
        
        if isinstance(feedback_sentiment_result, dict) and 'score' in feedback_sentiment_result and 'label' in feedback_sentiment_result:
            feedback_sentiment_score = feedback_sentiment_result['score']
            feedback_sentiment_label = feedback_sentiment_result['label']
        else:
            print(f"ERROR: Invalid sentiment output for {employee_id} feedback: {feedback_sentiment_result}")
            feedback_sentiment_score = 0.5
            feedback_sentiment_weight = 1.0
    else:
        print(f"WARNING: Employee {employee_id} has no past feedback.")
        feedback_sentiment_score = 0.5 

    senor_data = pd.read_csv('data_pipeline/sensory_data.csv')
    stress_score = calculate_stress_score(senor_data, employee_id)
    productivity_score = employee.get("normalized_productivity_score", 0.5)


    burnout_score = calculate_burnout( 
        feedback_sentiment_score ,  
        email_sentiment_score,
        stress_score,
        productivity_score
    )


    employee["burnout_score"] = burnout_score
    employee["email_sentiment_score"] = email_sentiment_score
    employee["feedback_sentiment_score"] = feedback_sentiment_score
    employee["email_sentiment_label"] = categorize_sentiment_label(email_sentiment_score)
    employee["feedback_sentiment_label"] = categorize_sentiment_label(feedback_sentiment_score)
    employee["stress_score"] = stress_score

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return {
        "employee_id": employee_id,
        "burnout_score": burnout_score,
        "email_sentiment_score": email_sentiment_score,
        "feedback_sentiment_score": feedback_sentiment_score,
        "email_sentiment_label": employee["email_sentiment_label"],
        "feedback_sentiment_label": employee["feedback_sentiment_label"],
        "stress_score": employee["stress_score"],
        "productivity_score": productivity_score
    }