import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import psycopg


load_dotenv(os.path.join('TRIAL_JWT', '.env'))

# SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL_PG")
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://samirpadekar:Honcho2025@localhost/honcho"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
