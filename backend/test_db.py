from sqlalchemy import text
from database import engine

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        print("? РџРѕРґРєР»СЋС‡РµРЅРёРµ СѓСЃРїРµС€РЅРѕ!")
        print(result.fetchone())
except Exception as e:
    print("? РћС€РёР±РєР° РїРѕРґРєР»СЋС‡РµРЅРёСЏ:")
    print(e)
