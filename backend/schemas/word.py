from typing import Optional
from pydantic import BaseModel


class WordBase(BaseModel):
    english: str
    russian: str
    category: str = "common"
    difficulty: int = 1

class WordCreate(WordBase):
    pass

class WordUpdate(WordBase):
    pass

class WordResponse(WordBase):
    id: int

    class Config:
        from_attributes = True

class WordPartialUpdate(BaseModel):
    english: Optional[str] = None
    russian: Optional[str] = None
    category: Optional[str] = None
    difficulty: Optional[int] = None