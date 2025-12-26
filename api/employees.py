from fastapi import APIRouter, HTTPException
import json
import os
router = APIRouter()

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data_pipeline/synthetic_employees.json")

@router.get("/employees")
def get_all_employees():
    """Fetch all employees with their details, including health data."""
    if not os.path.exists(DATA_FILE):
        raise HTTPException(status_code=404, detail="Employee data file not found.")

    try:
        with open(DATA_FILE, "r") as f:
            employees = json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error parsing employee data file.")

    for emp in employees:
        emp_id = emp.get("id")

    return {"employees": employees}

@router.get("/employee/{employee_id}")
def get_employee(employee_id: str):
    """Fetch a specific employee's details with health data."""
    if not os.path.exists(DATA_FILE):
        raise HTTPException(status_code=404, detail="Employee data file not found.")

    try:
        with open(DATA_FILE, "r") as f:
            employees = json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error parsing employee data file.")

    # Find employee by ID
    employee = next((emp for emp in employees if emp.get("id") == employee_id), None)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found.")

    return {"employee": employee}
