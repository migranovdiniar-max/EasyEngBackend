from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.word import Word
from models.user_progress import UserProgress
from datetime import datetime, timedelta
import random
from routers.auth import get_current_user


router = APIRouter(
    prefix="/learn", tags=["learning"]
)

@router.get("/next")
def get_next_word(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    due_words = (
        db.query(Word)
        .join(UserProgress, Word.id == UserProgress.word_id)
        .filter(
            UserProgress.user_id == current_user.id,
            UserProgress.next_review <= datetime.now(),
            UserProgress.known == True
        )
        .all()
    )

    new_words = (
        db.query(Word)
        .outerjoin(
            UserProgress, (UserProgress.word_id == Word.id) & (UserProgress.user_id == current_user.id)
        )
        .filter(UserProgress.id.is_(None))
        .all()
    )

    if due_words:
        wod = random.choice(due_words)
        return {
            "id": wod.id,
            "en": wod.en,
            "ru": wod.ru,
            "type": "review"
        }
    
    if new_words:
        wod = random.choice(new_words)
        return {
            "id": wod.id,
            "en": wod.english,
            "ru": wod.russian,
            "type": "new"
        }
    
    raise HTTPException(status_code=404, detail="No words found")


@router.post("/known/{word_id}")
def mark_word_known(
    word_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    progress = (
        db.query(UserProgress)
        .filter(UserProgress.user_id == current_user.id, UserProgress.word_id == word_id)
        .first()
    )

    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            word_id=word_id,
            known=True,
            interval=1,
            ease_factor=2.5,
            last_reviewed=datetime.utcnow(),
            next_review=datetime.utcnow() + timedelta(days=1)
        )
        db.add(progress)
    else:
        progress.interval = max(
            1, int(progress.interval * progress.ease_factor)
        )
        progress.last_reviewed = datetime.utcnow()
        progress.next_review = datetime.utcnow() + timedelta(days=progress.interval)

    db.commit()
    return {
        "status": "success",
        "next_review_in_days": f"{progress.interval} days"
    }