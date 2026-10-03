from database import SessionLocal, engine
from models import Base, Attendance


# create table if not exists
Base.metadata.create_all(bind=engine)


db = SessionLocal()


attendance_records = [

    Attendance(
        employee_id="EMP001",
        date="2026-07-21",
        status="Present"
    ),

    Attendance(
        employee_id="EMP001",
        date="2026-07-20",
        status="Present"
    ),

    Attendance(
        employee_id="EMP001",
        date="2026-07-19",
        status="Absent"
    )

]


db.add_all(attendance_records)

db.commit()


print("Attendance records created successfully")


db.close()