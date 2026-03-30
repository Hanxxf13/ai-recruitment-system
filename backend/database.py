from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./backend/data/recruitment.db")

# Automatically fix postgres:// to postgresql:// as required by SQLAlchemy 1.4+
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Ensure the directory for the database exists if using sqlite
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    db_dir = os.path.dirname(DATABASE_URL.replace("sqlite:///", ""))
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL, connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
