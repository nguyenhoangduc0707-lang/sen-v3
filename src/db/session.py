import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.config import settings

DATABASE_URL = os.getenv("DATABASE_URL", settings.DATABASE_URL)

# detect sqlite and set check_same_thread and WAL
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Create engine
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# ensure WAL for sqlite
if DATABASE_URL.startswith("sqlite"):
    try:
        with engine.connect() as conn:
            conn.execute(text("PRAGMA journal_mode=WAL"))
    except Exception:
        pass

SessionLocal = sessionmaker(bind=engine)


def get_engine():
    return engine


def get_session():
    return SessionLocal()
