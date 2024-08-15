from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from data.config import DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from utils.db_api.models import Base
    Base.metadata.create_all(bind=engine)
