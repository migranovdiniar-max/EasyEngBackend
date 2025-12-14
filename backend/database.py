from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base  # ? импортируем, но не создаём
import os

# Сначала создаём Base
Base = declarative_base()

# Теперь можно импортировать модели (они используют Base)
from models.user import User
from models.word import Word
from models.user_progress import UserProgress
from models.quiz_result import QuizResult

# Теперь подключаемся к БД
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/EasyEngAPP"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Оставь get_db() как есть
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
