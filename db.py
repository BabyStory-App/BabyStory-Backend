from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from core.env import env


def create_db_sessionLocal():
    DB_URL = f'mysql+pymysql://{env.get("MYSQL_USER")}:{env.get("MYSQL_PASSWORD")}@{env.get("MYSQL_HOST")}:{env.get("MYSQL_PORT")}/{env.get("MYSQL_DATABASE")}'

    engine = create_engine(DB_URL, pool_size=20, max_overflow=20)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


SessionLocal = create_db_sessionLocal()
DB_Base = declarative_base()

# Dependency
# try finally문을 통해 db 연결이 종료되거나 문제가 생겼을 때 무조건 close 해준다.
# db 연결 과정에서 생긴 문제가 아닌 경우 아래에 except를 추가하여도 처리되지 않는다.


def get_db_session():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()
