import os

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "yoklama.db")
SQLALCHEMY_DATABASE_URL = "sqlite:///" + DB_PATH.replace("\\", "/")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def ensure_schema():
    """Mevcut veritabanlarına yeni sütunları ekler."""
    inspector = inspect(engine)
    if "ogrenciler" not in inspector.get_table_names():
        return

    kolonlar = {kolon["name"] for kolon in inspector.get_columns("ogrenciler")}
    if "veli_tel" not in kolonlar:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE ogrenciler ADD COLUMN veli_tel VARCHAR"))

    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE ogrenciler
            SET veli_tel = '+9055510' || printf('%04d', id)
            WHERE veli_tel IS NULL OR veli_tel = ''
        """))
