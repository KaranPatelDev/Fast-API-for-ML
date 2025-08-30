from sqlalchemy.orm import Session
import models,schemas

def get_employees(db: Session):
    return db.query(models.Employee).all()

def get_employee_by_id(db: Session, emp_id: int):
    return (
        db
        .query(models.Employee)
        .filter(models.Employee.id == emp_id)
        .first() #This will return only one record or None if not found
    )

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(
        name=employee.name,
        email=employee.email
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee) #To get the generated ID and other defaults
    return db_employee


def update_employee(db: Session, emp_id: int, employee: schemas.EmployeeUpdate):
    db_employee = (
        db.query(models.Employee)
        .filter(models.Employee.id == emp_id)
        .first()
    )
    if db_employee:
        db_employee.name = employee.name
        db_employee.email = employee.email
        db.commit()
        db.refresh(db_employee)
    return db_employee

def delete_employee(db: Session, emp_id: int):
    db_employee = (
        db.query(models.Employee)
        .filter(models.Employee.id == emp_id)
        .first()
    )
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee # Return the deleted employee or None if not found
