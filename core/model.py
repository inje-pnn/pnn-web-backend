from sqlalchemy import Column, ForeignKey, String, Integer
from core.database import Base
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = "users"



class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)       # 프로젝트 ID
    memberid = Column(String(255), ForeignKey("members.email"), nullable=False)  # 외래 키 (members.email)
    title = Column(String(255), nullable=False)              # 프로젝트 제목
    postdate = Column(String(255), nullable=False)           # 프로젝트 게시 날짜
    project_type = Column(String(50), nullable=False)        # 프로젝트 타입
    link = Column(String(2083), nullable=True)               # 프로젝트 링크
    add_content = Column(String(50), nullable=True)          # 추가 설명
    image = Column(String(2083), nullable=True)              # 이미지 주소

    # 관계 설정 (Optional: users 테이블과 연계)
    users = relationship("UserModel", back_populates="projects")