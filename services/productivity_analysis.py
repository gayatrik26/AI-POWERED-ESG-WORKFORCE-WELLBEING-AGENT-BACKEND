import pandas as pd
import os
import json

def calculate_productivity_score(df):
    # Define weight coefficients for each factor
    weights = {
        "projects_handled": 2.0,
        "working_hours": 1.5,
        "overtime_hours": 1.2,
        "sick_days": -2.0,
        "training_hours": 1.0,
        "remote_work_frequency": 0.8,
        "employee_satisfaction_score": 1.5,
        "meeting_overload": -1.5
    }

    # Compute productivity score using the formula
    df["productivity_score"] = (
        weights["projects_handled"] * df["projects_handled"] +
        weights["working_hours"] * df["working_hours"] +
        weights["overtime_hours"] * df["overtime_hours"] +
        weights["sick_days"] * df["sick_days"] +
        weights["training_hours"] * df["training_hours"] +
        weights["remote_work_frequency"] * df["remote_work_frequency"] +
        weights["employee_satisfaction_score"] * df["employee_satisfaction_score"] +
        weights["meeting_overload"] * df["meeting_overload"]
    )
    min_score = df["productivity_score"].min()
    max_score = df["productivity_score"].max()
    df["normalized_productivity_score"] = (df["productivity_score"] - min_score) / (max_score - min_score)
    emp = df
    DATA_FILE = os.path.join(os.path.dirname(__file__), "../data_pipeline/synthetic_employees.json")

    with open(DATA_FILE, "r") as f:
            data = json.load(f)

    # Update the JSON file with the new productivity scores
    for i, emp in df.iterrows():
        for e in data:
            if e["id"] == emp["employee_id"]:
                # e["productivity_score"] = emp["productivity_score"]
                e["normalized_productivity_score"] = emp["normalized_productivity_score"]
                e["meeting_overload"] = emp["meeting_overload"]
                e["working_hours"] = emp["working_hours"]
                e["overtime_hours"] = emp["overtime_hours"]
                e["employee_satisfaction_score"] = emp["employee_satisfaction_score"]
                break


    with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
            print("[INFO] JSON file updated successfully.")

    return emp


# df = pd.read_csv("/Users/kdn_aigayatrikadam/Desktop/Projects/ESG Wellbeing Agent/backend/data_pipeline/productivity_data.csv")
# df = calculate_productivity_score(df)
# print(df[["employee_id", "normalized_productivity_score"]])