###
from sqlalchemy.orm import Session
from core.model import UserModel  # 데이터베이스 모델로 변경
from fastapi import HTTPException
from typing import Optional

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, payload):
        if self.get_user_by_email(payload.email):
            raise HTTPException(status_code=400, detail="Email already registered")

        db_user = UserModel(
            name=payload.name,
            email=payload.email,
            student_id=payload.student_id,
            year=payload.year,
            github_url=payload.github_url,
        )
        self.session.add(db_user)
        self.session.commit()
        return payload.email

    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        return self.session.query(UserModel).filter(UserModel.email == email).first()

    def update_user_info(self, email: str, student_id: str, year: int, github_url: Optional[str] = None):
        user = self.get_user_by_email(email)
        if user:
            user.student_id = student_id
            user.year = year
            user.github_url = github_url
            self.session.commit()

