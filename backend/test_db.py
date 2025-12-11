from sqlalchemy import text
from database import engine

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        print("? Подключение успешно!")
        print(result.fetchone())
except Exception as e:
    print("? Ошибка подключения:")
    print(e)
