###
from sqlalchemy import Column, String, Integer
from core.database import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)  
    token = Column(String(255), nullable=True)
    student_number = Column(String(50), unique=True, nullable=True)
    student_grade = Column(Integer, nullable=True)
    name = Column(String(255), nullable=True)
    github_url = Column(String(255), nullable=True)
