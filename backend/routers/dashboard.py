from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
import math
from sqlalchemy import func

from database import get_db
from models.user import User
from models.word import Word
from models.user_progress import UserProgress
from .auth import get_current_user  # или из auth.py

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Общее количество слов
    total_words = db.query(Word).count()

    # Количество выученных слов (known = True)
    learned_words = (
        db.query(UserProgress)
        .filter(UserProgress.user_id == current_user.id, UserProgress.known == True)
        .count()
    )

    # Слова, которые пора повторять (next_review <= now)
    due_words = (
        db.query(UserProgress)
        .filter(
            UserProgress.user_id == current_user.id,
            UserProgress.next_review <= datetime.utcnow(),
            UserProgress.known == True
        )
        .count()
    )

    # -----------------------------------------------
    # ?? Подсчёт страйка (дней подряд)
    # -----------------------------------------------

    # Сначала получим все даты, когда пользователь повторял слова (с known=True)
    review_dates = (
        db.query(
            func.date(UserProgress.last_reviewed)
        )
        .filter(
            UserProgress.user_id == current_user.id,
            UserProgress.known == True
        )
        .distinct()
        .order_by(func.date(UserProgress.last_reviewed).desc())
        .all()
    )

    # Преобразуем в список дат
    review_dates = [r[0] for r in review_dates]  # [(date,), ...] -> [date, ...]

    from datetime import date, timedelta

    if not review_dates:
        streak = 0
    else:
        today = date.today()
        yesterday = today - timedelta(days=1)

        # Проверим, активен ли сегодня
        has_reviewed_today = today in review_dates

        # Если не активен — страйк обнуляется
        if not has_reviewed_today:
            # Считаем, сколько дней подряд до вчера
            streak = 0
            expected_date = yesterday
            for d in review_dates:
                if d == expected_date:
                    streak += 1
                    expected_date -= timedelta(days=1)
                else:
                    break
        else:
            # Активен сегодня — считаем с сегодняшнего дня
            streak = 1
            expected_date = today - timedelta(days=1)  # вчера
            for d in review_dates[1:]:  # пропускаем сегодня
                if d == expected_date:
                    streak += 1
                    expected_date -= timedelta(days=1)
                else:
                    break

    return {
        "total_words": total_words,
        "learned_words": learned_words,
        "due_words": due_words,
        "streak": streak
    }
