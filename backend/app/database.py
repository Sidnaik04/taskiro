from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from .config import settings


def _normalize_db_url(url: str) -> str:
    # Heroku might supply "postgres://", SQLAlchemy 2.x wants "postgresql+psycopg2://"
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg2://", 1)
    # Enforce SSL on Heroku Postgres
    if "heroku" in url and "sslmode=" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}sslmode=require"
    return url


DATABASE_URL = (
    settings.database_url or os.getenv("DATABASE_URL") or "sqlite:///./local.db"
)
DATABASE_URL = _normalize_db_url(DATABASE_URL)

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
