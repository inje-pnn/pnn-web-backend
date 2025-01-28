from sqlalchemy import Column, ForeignKey, String, Integer
from core.database import Base
from sqlalchemy.orm import relationship


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

    project = relationship("ProjectModel", back_populates="user")


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)       # 프로젝트 ID
    memberid = Column(String(255), ForeignKey("users.email", ondelete="CASCADE"), nullable=False)  # 외래 키 (users.email)
    title = Column(String(255), nullable=False)              # 프로젝트 제목
    sub_title = Column(String(255), nullable=False)          # 서브타이틀
    project_type = Column(String(50), nullable=False)        # 프로젝트 타입
    project_category = Column(String(50), nullable=False)     # 프로젝트 유형형
    link = Column(String(2083), nullable=True)               # 프로젝트 링크
    image = Column(String(2083), nullable=True)              # 이미지 주소
    
    # 관계 설정 (users 테이블과 연계)
    user = relationship("UserModel", back_populates="project")