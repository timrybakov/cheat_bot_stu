from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    user_telegram_id = Column(Integer, nullable=False)
    bucket = Column(String(255), nullable=False)
    file_path = Column(String(255), nullable=False)
    image_id = Column(String(255), nullable=False)
    file_unique_id = Column(String(255), unique=True, nullable=False)
