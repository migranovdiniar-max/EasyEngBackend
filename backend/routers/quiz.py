from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from random import sample
from datetime import datetime, timedelta
import random

from database import get_db
from models.user import User
from models.word import Word
from models.user_progress import UserProgress
from routers.auth import get_current_user

router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.get("/next")
def get_quiz_word(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    all_words = db.query(Word).all()
    if len(all_words) < 4:
        raise HTTPException(
            status_code=400,
            detail="Not enough words in the database"
        )
    
    correct_word = random.choice(all_words)

    wrong_translations = [
        w.russian for w in all_words 
        if w.id != correct_word.id
    ]
    if len(wrong_translations) < 3:
        raise HTTPException(
            status_code=400,
            detail="Not enough words in the database"
        )
    
    selected_wrong = sample(wrong_translations, 3)

    options = [correct_word.russian] + selected_wrong
    random.shuffle(options)

    return {
        "word": correct_word.english,
        "options": options,
        "correct": None
    }


@router.post("/check")
def check_quiz_answer(
    en: str,
    selected_translation: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    word = db.query(Word).filter(Word.english == en).first()
    if not word:
        raise HTTPException(
            status_code=404,
            detail="Word not found"
        )
    
    is_correct = word.id == selected_translation

    progress = (
        db.query(UserProgress)
        .filter(
            UserProgress.user_id == current_user.id,
            UserProgress.word_id == word.id
        )
        .first()
    )

    if is_correct:
        if not progress:
            progress = UserProgress(
                user_id=current_user.id,
                word_id=word.id,
                known=True,
                interval=1,
                ease_factor=2.5,
                last_reviewed=datetime.utcnow(),
                next_review=datetime.utcnow() + timedelta(days=1)
            )
            db.add(progress)
        else:
            progress.known = True
            progress.interval = max(
                1, int(progress.interval * progress.ease_factor)
            )
            progress.last_reviewed = datetime.utcnow()
            progress.next_review = datetime.utcnow() + timedelta(days=progress.interval)
    else:
        if not progress:
            progress = UserProgress(
                user_id=current_user.id,
                word_id=word.id,
                known=False,
                interval=1,
                ease_factor=2.5,
                last_reviewed=datetime.utcnow(),
                next_review=datetime.utcnow() + timedelta(days=1)
            )
            db.add(progress)
        else:
            progress.known = False
            progress.interval = 1
            progress.last_reviewed = datetime.utcnow()
            progress.next_review = datetime.utcnow() + timedelta(days=1)
    db.commit()

    return {
        "correct": is_correct,
        "correct_translation": word.russian,
        "status": "success"
    }