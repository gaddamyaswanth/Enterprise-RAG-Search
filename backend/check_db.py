from database import SessionLocal
from models import Employee

db = SessionLocal()

employees = db.query(Employee).all()

print("Total employees:", len(employees))

for emp in employees:
    print(emp.employee_id, emp.name, emp.email)

db.close()