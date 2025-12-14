from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from database import get_db
from models.user import User
from models.word import Word
from models.user_progress import UserProgress
from models.quiz_result import QuizResult
from routers.auth import get_current_user

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("")
def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    categories = db.query(Word.category).distinct().all()
    categories = [cat[0] for cat in categories]

    words_by_category = {}

    for cat in categories:
        total = db.query(Word).filter(Word.category == cat).count()

        learned = (
            db.query(UserProgress)
            .join(Word, UserProgress.word_id == Word.id)
            .filter(
                UserProgress.user_id == current_user.id,
                Word.category == cat,
                UserProgress.known == True
            )
            .count()
        )

        words_by_category[cat] = {
            "learned": learned,
            "total": total
        }

    quiz_results = (
        db.query(QuizResult)
        .filter(QuizResult.user_id == current_user.id)
        .all()
    )

    total_quizzes = len(quiz_results)
    correct_quizzes = len([r for r in quiz_results if r.correct])

    quiz_accuracy = 0
    if total_quizzes > 0:
        quiz_accuracy = round((correct_quizzes / total_quizzes) * 100)

    total_words_learned = (
        db.query(UserProgress)
        .filter(UserProgress.user_id == current_user.id, UserProgress.known == True)
        .count()
    )

    last_review = (
        db.query(func.max(UserProgress.last_reviewed))
        .filter(UserProgress.user_id == current_user.id)
        .scalar()
    )

    last_quiz = (
        db.query(func.max(QuizResult.timestamp))
        .filter(QuizResult.user_id == current_user.id)
        .scalar()
    )

    last_activity = max(
        last_review or datetime.min,
        last_quiz or datetime.min
    )

    return {
        "words_by_category": words_by_category,
        "quiz_accuracy": f"{quiz_accuracy}%",
        "total_words_learned": total_words_learned,
        "total_quizzes": f"{total_quizzes}",
        "last_activity": last_activity.isoformat() if last_activity else None,
    }