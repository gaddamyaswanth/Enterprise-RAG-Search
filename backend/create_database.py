from database import SessionLocal, create_tables
from models import Employee
from auth import hash_password

create_tables()

db = SessionLocal()

employee = Employee(
    employee_id="EMP001",
    name="Yaswanth",
    email="yaswanth@company.com",
    password=hash_password("123456"),
    department="Data Science"
)

db.add(employee)
db.commit()

print("Employee created successfully")

db.close()