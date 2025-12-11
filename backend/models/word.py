from sqlalchemy import Column, Integer, String
from database import Base


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, index=True)
    english = Column(String, nullable=False)
    russian = Column(String, nullable=False)
    category = Column(String, default="common")
    difficulty = Column(Integer, default=1)