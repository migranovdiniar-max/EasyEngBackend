from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from models.word import Word
from schemas.word import WordResponse, WordCreate, WordUpdate, WordPartialUpdate
from database import get_db


router = APIRouter(
    prefix="/words", tags=["words"]
)

@router.get("/", response_model=List[WordResponse])
def get_words(db: Session = Depends(get_db)):
    return db.query(Word).all()


@router.get("/{word_id}", response_model=WordResponse)
def get_word(word_id: int, db: Session = Depends(get_db)):
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word not found"
        )
    return word


@router.post("/", response_model=WordResponse)
def create_word(word: WordCreate, db: Session = Depends(get_db)):
    db_word = Word(
        **word.model_dump()
    )
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word


@router.put("/{word_id}", response_model=WordResponse)
def update_word(word_id: int, word: WordUpdate, db: Session = Depends(get_db)):
    db_word = db.query(Word).filter(Word.id == word_id).first()
    if not db_word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word not found"
        )
    
    for key, value in word.model_dump().items():
        setattr(db_word, key, value)

    db.commit()
    db.refresh(db_word)
    return db_word


@router.delete("/{word_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_word(word_id: int, db: Session = Depends(get_db)):
    db_word = db.query(Word).filter(Word.id == word_id).first()
    if not db_word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word not found"
        )
    
    db.delete(db_word)
    db.commit()


@router.patch("/{word_id}", response_model=WordResponse)
def update_word_partial(
    word_id: int, 
    word_update: WordPartialUpdate,
    db: Session = Depends(get_db)
):
    db_word = db.query(Word).filter(Word.id == word_id).first()
    if not db_word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word not found"
        )
    
    update_data = word_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_word, key, value)

    db.commit()
    db.refresh(db_word)
    return db_word