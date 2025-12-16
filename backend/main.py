from fastapi import FastAPI
from database import engine, Base  # ? Base уже сюда импортируется
import models.word  # ? можно оставить, но не обязательно
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    word as word_router, 
    auth as user_router,
    learning as learning_router,
    dashboard as dashboard_router,
    quiz as quiz_router,
    stats as stats_router
)


app = FastAPI(title="EasyEng API")

# Создаём таблицы (если НЕ используем Alembic)
# Base.metadata.create_all(bind=engine)  # ? только если НЕ используем миграции

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ? разрешаем все домены
    allow_credentials=True,
    allow_methods=["*"],  # ? разрешаем все методы
    allow_headers=["*"],  # ? разрешаем все заголовки
)

app.include_router(word_router.router, prefix="/api")
app.include_router(user_router.router, prefix="/api")
app.include_router(learning_router.router, prefix="/api")
app.include_router(dashboard_router.router, prefix="/api")
app.include_router(quiz_router.router, prefix="/api")
app.include_router(stats_router.router, prefix="/api")

@app.get("/api")
def read_root():
    return {"message": "Welcome to EasyEng API"}
