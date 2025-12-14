from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Boolean, UniqueConstraint
from database import Base
from datetime import datetime


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)

    known = Column(Boolean, default=False)
    next_review = Column(DateTime, default=datetime.utcnow)
    ease_factor = Column(Float, default=2.5)
    interval = Column(Integer, default=1)
    last_reviewed = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("user_id", "word_id", name="unique_user_word"),
    )

    