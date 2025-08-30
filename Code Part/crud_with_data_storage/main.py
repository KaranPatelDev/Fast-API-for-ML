from fastapi import FastAPI, HTTPException
from models import Employee
from typing import List
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "./employees_db.json")

def load_employees():
    if not os.path.exists(DB_PATH):
        return []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Employee(**emp) for emp in data]

def save_employees(employees: List[Employee]):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump([emp.dict() for emp in employees], f, indent=4)

employees_db: List[Employee] = load_employees()

app = FastAPI()


# 1. Read all employees
@app.get('/employees', response_model=List[Employee])
def get_employees():
    return employees_db


# 2. Read specific employee
@app.get('/employees/{emp_id}', response_model=Employee)
def get_employee(emp_id: int):
    for index, employee in enumerate(employees_db):
        if employee.id == emp_id:
            return employees_db[index]
    raise HTTPException(status_code=404, detail='Employee Not Found')


# 3. Add an employee
@app.post('/add_employee', response_model=Employee)
def add_employee(new_emp: Employee):
    for employee in employees_db:
        if employee.id == new_emp.id:
            raise HTTPException(status_code=400, detail='Employee already exists')
    employees_db.append(new_emp)
    save_employees(employees_db)
    return new_emp


# 4. Update an employee
@app.put('/update_employee/{emp_id}', response_model=Employee)
def update_employee(emp_id: int, updated_employee: Employee):
    for index, employee in enumerate(employees_db):
        if employee.id == emp_id:
            employees_db[index] = updated_employee
            save_employees(employees_db)
            return updated_employee
    raise HTTPException(status_code=404, detail='Employee Not Found')


# 5. Delete an employee
@app.delete('/delete_employee/{emp_id}')
def delete_employee(emp_id: int):
    for index, employee in enumerate(employees_db):
        if employee.id == emp_id:
            del employees_db[index]
            save_employees(employees_db)
            return {'message': 'Employee deleted successfully'}
    raise HTTPException(status_code=404, detail='Employee Not Found')
