from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.quiz_result import QuizResult
from database import get_db
from models.user import User
from models.word import Word
from models.user_progress import UserProgress
from datetime import datetime, timedelta
import random
from routers.auth import get_current_user
from sqlalchemy import func


router = APIRouter(
    prefix="/learn", tags=["learning"]
)


@router.get("/next")
def get_next_word(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Получаем слова, которые пора повторять
    due_words = (
        db.query(Word)
        .join(UserProgress, Word.id == UserProgress.word_id)
        .filter(
            UserProgress.user_id == current_user.id,
            UserProgress.next_review <= datetime.utcnow(),
            UserProgress.known == True
        )
        .all()
    )

    # 2. Если есть due_words — применяем "умную" сортировку
    if due_words:
        # ?????? НАЧАЛО: анализ точности по викторине ??????
        word_accuracy = {}

        # Группируем результаты викторины по слову
        quiz_results = (
            db.query(
                QuizResult.word_id,
                func.count(QuizResult.id).label("total"),
                func.sum(QuizResult.correct).label("correct")
            )
            .filter(QuizResult.user_id == current_user.id)
            .group_by(QuizResult.word_id)
            .all()
        )

        # Считаем accuracy для каждого слова
        for res in quiz_results:
            accuracy = res.correct / res.total if res.total > 0 else 0
            word_accuracy[res.word_id] = accuracy

        # Сортируем: чем ХУЖЕ accuracy — тем ВЫШЕ приоритет (раньше в списке)
        # Т.е. сортируем по возрастанию accuracy (0.2 ? 0.5 ? 1.0)
        due_words.sort(key=lambda word: word_accuracy.get(word.id, 0))  # ?

        # Берём слово с наихудшей точностью
        wod = due_words[0]
        return {
            "id": wod.id,
            "en": wod.english,
            "ru": wod.russian,
            "type": "review",
            "accuracy": round(word_accuracy.get(wod.id, 0), 2)  # можно вернуть
        }

    # 3. Новые слова
    new_words = (
        db.query(Word)
        .outerjoin(
            UserProgress,
            (UserProgress.word_id == Word.id) & (UserProgress.user_id == current_user.id)
        )
        .filter(UserProgress.id.is_(None))
        .all()
    )

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
        progress.known = True
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


@router.post("/unknown/{word_id}")
def mark_word_unknown(
    word_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    progress = (
        db.query(UserProgress)
        .filter(
            UserProgress.user_id == current_user.id, 
            UserProgress.word_id == word_id)
        .first())
    
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
        "status": "success",
        "message": "Word will be reviewed again in 1 day",
        "next_review_in_days": "1 day"
    }