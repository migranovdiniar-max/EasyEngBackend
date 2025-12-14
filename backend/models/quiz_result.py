from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from database import Base
from datetime import datetime


class QuizResult(Base):
    __tablename__ = 'quiz_results'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    word_id = Column(Integer, ForeignKey('words.id'), nullable=False)
    correct = Column(Boolean, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)