###
from sqlalchemy import Column, String, Integer
from core.database import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)  
    token = Column(String(255), nullable=False)  
    student_id = Column(String(50), unique=True, nullable=False)  #학번
    year = Column(Integer, nullable=False)  #학년
    name = Column(String(255), nullable=False)  #이름
    github_url = Column(String(255), nullable=True)