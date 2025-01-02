from sqlalchemy import Column, String, Integer
from core.database import Base

class UserModel(Base):
    __tablename__ = "users"