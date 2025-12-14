from fastapi import FastAPI
from database import engine, Base  # ? Base уже сюда импортируется
import models.word  # ? можно оставить, но не обязательно
from routers import (
    word as word_router, 
    auth as user_router,
    learning as learning_router
)


app = FastAPI(title="EasyEng API")

# Создаём таблицы (если НЕ используем Alembic)
# Base.metadata.create_all(bind=engine)  # ? только если НЕ используем миграции

app.include_router(word_router.router)
app.include_router(user_router.router)
app.include_router(learning_router.router)

@app.get("/api")
def read_root():
    return {"message": "Welcome to EasyEng API"}
