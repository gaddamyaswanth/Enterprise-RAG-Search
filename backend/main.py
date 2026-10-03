from fastapi import FastAPI
from pydantic import BaseModel

from database import SessionLocal
from models import Employee, Leave, Attendance
from auth import verify_password


app = FastAPI(
    title="Enterprise Employee Management System"
)



# ================= HOME =================

@app.get("/")
def home():

    return {
        "message": "Employee Management API Running"
    }



# ================= LOGIN =================


class LoginData(BaseModel):

    email: str
    password: str



@app.post("/login")
def login(data: LoginData):

    db = SessionLocal()


    employee = db.query(Employee).filter(
        Employee.email == data.email
    ).first()



    if not employee:

        db.close()

        return {
            "error": "Employee not found"
        }



    if verify_password(
        data.password,
        employee.password
    ):

        result = {

            "message": "Login successful",

            "employee": employee.name,

            "department": employee.department,

            "role": employee.role

        }

        db.close()

        return result



    db.close()


    return {
        "error": "Invalid password"
    }





# ================= EMPLOYEE PROFILE =================


@app.get("/employee/{employee_id}")
def employee_profile(employee_id:str):

    db = SessionLocal()


    employee = db.query(Employee).filter(
        Employee.employee_id == employee_id
    ).first()



    if not employee:

        return {
            "error":"Employee not found"
        }



    leave = db.query(Leave).filter(
        Leave.employee_id == employee_id
    ).first()



    if leave:

        leave_info = {

            "total_leaves": leave.total_leaves,

            "used_leaves": leave.used_leaves,

            "remaining_leaves":
            leave.total_leaves - leave.used_leaves

        }


    else:

        leave_info = {

            "total_leaves":0,

            "used_leaves":0,

            "remaining_leaves":0

        }




    db.close()



    return {


        "employee":{

            "id":employee.employee_id,

            "name":employee.name,

            "email":employee.email,

            "department":employee.department,

            "role":employee.role

        },


        "leave":leave_info

    }




# ================= ATTENDANCE =================


@app.get("/attendance/{employee_id}")
def attendance(employee_id:str):

    db = SessionLocal()


    records = db.query(Attendance).filter(

        Attendance.employee_id == employee_id

    ).all()



    total_days = len(records)



    present = len(
        [
            x for x in records
            if x.status=="Present"
        ]
    )


    absent = len(
        [
            x for x in records
            if x.status=="Absent"
        ]
    )



    db.close()



    return {


        "employee_id":employee_id,

        "total_days":total_days,

        "present_days":present,

        "absent_days":absent,

        "attendance_percentage":

        round((present/total_days)*100,2)

        if total_days>0 else 0


    }





# ================= SEARCH =================


class SearchRequest(BaseModel):

    query:str



@app.post("/search")
def search(data:SearchRequest):


    documents=[

        "Data Science team builds machine learning models.",

        "HR manages employee attendance and leaves.",

        "Engineering develops software applications."

    ]


    result=[]


    for doc in documents:

        if data.query.lower() in doc.lower():

            result.append(doc)



    return {

        "query":data.query,

        "results":result

    }