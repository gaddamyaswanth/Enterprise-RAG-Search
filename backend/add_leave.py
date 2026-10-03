from database import SessionLocal, engine
from models import Base
from sqlalchemy import Column, Integer, String


class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True)
    employee_id = Column(String)
    total_leaves = Column(Integer)
    used_leaves = Column(Integer)


Base.metadata.create_all(bind=engine)


db = SessionLocal()


leave = Leave(
    employee_id="EMP001",
    total_leaves=24,
    used_leaves=5
)


db.add(leave)
db.commit()

print("Leave record created")

db.close()