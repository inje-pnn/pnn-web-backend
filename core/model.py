from sqlalchemy import JSON, Column, ForeignKey, String, Integer, Text, DateTime
from core.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)  
    token = Column(String(255), nullable=True)
    student_number = Column(String(50), nullable=True)
    student_grade = Column(Integer, nullable=True)
    name = Column(String(255), nullable=True)
    github_url = Column(String(255), nullable=True)
    authority = Column(Integer, nullable=False, default=3)
    image_url = Column(String(500), nullable=True)

    project = relationship("ProjectModel", back_populates="user")


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)       # 프로젝트 ID
    memberid = Column(String(255), ForeignKey("users.email", ondelete="CASCADE"), nullable=False)  # 외래 키 (users.email)
    title = Column(String(255), nullable=False)              # 프로젝트 제목
    sub_title = Column(String(255), nullable=False)          # 서브타이틀
    project_type = Column(JSON)                             
    project_category = Column(String(50), nullable=False)     # 프로젝트 유형
    project_tag = Column(String(50), nullable=False)         # 프로젝트 태그
    create_data = Column(String(50), nullable=False)
    link = Column(String(2083), nullable=True)               # 프로젝트 링크
    image = Column(String(2083), nullable=True)              # 이미지 주소
    
    # 관계 설정 (users 테이블과 연계)
    user = relationship("UserModel", back_populates="project")

class StudyPostModel(Base):
    __tablename__ = "studyboard"

    serial_number = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    username = Column(String(255), nullable=True)
    project_type = Column(JSON)
    project_category = Column(String(50), nullable=False)
    content_link = Column(Text, nullable=False)
    image = Column(String(255))
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

class AccountShareModel(Base):
    __tablename__ = "accountshareboard"

    serial_number = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    account_id  = Column(String(100), nullable=False)
    account_password  = Column(String(100), nullable=False)
    sharer = Column(String(255), nullable=False)
    sharername = Column(String(255), nullable=False)
    username = Column(JSON)
    content_link = Column(Text, nullable=False)
    image = Column(String(255))
    description = Column(String(255))