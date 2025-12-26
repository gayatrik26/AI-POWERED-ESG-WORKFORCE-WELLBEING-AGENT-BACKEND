import pandas as pd
import os
import json

def calculate_dominant_keyboard_emotion(df):
    """
    Calculate the dominant emotion for each user based on Affectiva emotion data.

    Parameters:
        df (pd.DataFrame): The input dataframe containing time-series emotion data.

    Returns:
        pd.DataFrame: A dataframe with users and their dominant emotion.
    """

    # Drop manual emotion columns (keeping only Affectiva emotion columns)
    affectiva_emotion_columns = [col for col in df.columns if col.startswith("emotion_affectiva_")]

    # Group by user and calculate the mean for Affectiva emotion columns
    user_emotions = df.groupby("session")[affectiva_emotion_columns].mean().reset_index()

    # Find the dominant emotion for each user (emotion with the highest mean value)
    user_emotions["dominant_emotion"] = user_emotions[affectiva_emotion_columns].idxmax(axis=1)

    # Clean up the emotion column names (remove prefix 'emotion_affectiva_')
    user_emotions["dominant_emotion"] = user_emotions["dominant_emotion"].str.replace("emotion_affectiva_", "", regex=True)

    # Ensure 'session' column exists before generating 'emp_id'
    if "session" not in user_emotions.columns:
        raise KeyError("Column 'session' is missing in the grouped DataFrame.")

    # Create 'emp_id' column correctly
    user_emotions["emp_id"] = "i100" + (11 + user_emotions["session"]).astype(str)

    DATA_FILE = os.path.join(os.path.dirname(__file__), "../data_pipeline/synthetic_employees.json")

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    # Correct iterating over the DataFrame
    for _, row in user_emotions.iterrows():  # Changed 'user_emotions' to 'row'
        for e in data:
            if e["id"] == row["emp_id"]:  # Using 'row' instead of overwriting 'user_emotions'
                e["keyboard_emotion"] = row["dominant_emotion"]
                break

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
        print("[INFO] JSON file updated successfully.")

    return user_emotions[["emp_id", "dominant_emotion"]]  # Fixed column name

# Example usage
# df = pd.read_excel("/Users/kdn_aigayatrikadam/Desktop/Projects/ESG Wellbeing Agent/backend/data_pipeline/keyboard_employee.xlsx")  
# user_emotion_summary = calculate_dominant_keyboard_emotion(df)
# print(user_emotion_summary)