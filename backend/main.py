from fastapi import FastAPI
from database import engine, Base
import models.word
from routers import word as word_router, auth as user_router


app = FastAPI(
    title="EasyEng API",
)

Base.metadata.create_all(bind=engine)

app.include_router(word_router.router)
app.include_router(user_router.router)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to EasyEng API"
    }