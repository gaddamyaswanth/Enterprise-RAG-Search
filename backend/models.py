from sqlalchemy import Column, Integer, String, Date, ForeignKey
from database import Base


class Employee(Base):

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)

    employee_id = Column(String, unique=True)

    name = Column(String)

    email = Column(String, unique=True)

    password = Column(String)

    department = Column(String)

    role = Column(String)

    joining_date = Column(String)


class Leave(Base):

    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True)

    employee_id = Column(String)

    total_leaves = Column(Integer)

    used_leaves = Column(Integer)


class Attendance(Base):

    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)

    employee_id = Column(String)

    date = Column(String)

    status = Column(String)