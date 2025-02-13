from sqlalchemy import create_engine

from sqlalchemy.orm import DeclarativeBase,sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:tonikr8s@localhost:5432/blog"
# connect_args = {"check_same_thread": False}


engine = create_engine(SQLALCHEMY_DATABASE_URL,)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()