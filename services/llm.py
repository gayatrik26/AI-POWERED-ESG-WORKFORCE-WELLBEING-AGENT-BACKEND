import openai
import os
import json
from services.cv_emotion import analyze_employee_images



DATA_FILE = os.path.join(os.path.dirname(__file__), "../data_pipeline/synthetic_employees.json")

def save_emotions_to_json(employee_id, emotions):
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        
        found = False
        for emp in data:
            if str(emp["id"]) == str(employee_id):
                emp["detected_emotions"] = emotions
                found = True
                print(f"[SUCCESS] Saved emotions for employee {employee_id}.")
                break

        if not found:
            print(f"[WARN] Employee ID {employee_id} not found in JSON.")
            return False

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
            print("[INFO] JSON file updated successfully.")
        return True
    except Exception as e:
        print(f"[ERROR] While saving emotions: {e}")
        return False

def generate_wellness_program(emp_info, employee_id):
    """
    Generates a personalized wellness program for the employee, including emotion analysis.
    """
    print(f"Analyzing images for employee ID: {employee_id}")
    emotions = analyze_employee_images(employee_id)

    if 'error' in emotions:
        print(f"Error analyzing emotions for {employee_id}: {emotions['error']}")
        return None

    save_emotions_to_json(employee_id, emotions)

    employee_data = f"""
    Employee Name: {emp_info['name']}
    Working Hours: {emp_info['working_hours']}
    Meeting Overload: {emp_info['meeting_overload']}
    HR Feedback: {emp_info['hr_feedback']}
    Burnout Score: {emp_info['burnout_score']}
    Email Sentiment Score: {emp_info['email_sentiment_score']}
    Email Sentiment Labels: {emp_info['email_sentiment_label']}
    Detected Emotions from Images: 
    """
    
    for img_name, emotion in emotions.items():
        employee_data += f"\n  - {img_name}: {emotion}"

    print("Employee Data Prepared for LLM:")
    print(employee_data)

    try:
        print("Calling OpenAI API...")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI assistant helping HR teams with employee wellness."},
                {"role": "user", "content": f"Generate a personalized wellness program for the following employee in 1-2 lines, don't give specification on time: {employee_data}"}
            ]
        )
        
        print("API Response Received.")
        wellness_program = response['choices'][0]['message']['content']
        print("Generated Wellness Program:")
        print(wellness_program)
        
        return wellness_program
    except openai.error.OpenAIError as e:
        print(f"Error generating wellness program: {e}")
        return None