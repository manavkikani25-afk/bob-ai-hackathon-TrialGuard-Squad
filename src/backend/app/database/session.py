import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_DB_FILE = os.path.join(BASE_DIR, 'trialguard.db')

if os.environ.get("VERCEL"):
    tmp_db_path = "/tmp/trialguard.db"
    if os.path.exists(DEFAULT_DB_FILE) and not os.path.exists(tmp_db_path):
        import shutil
        shutil.copyfile(DEFAULT_DB_FILE, tmp_db_path)
    DEFAULT_DB = f"sqlite:///{tmp_db_path}"
else:
    DEFAULT_DB = f"sqlite:///{DEFAULT_DB_FILE}"

DB_PATH = os.environ.get("DATABASE_URL", DEFAULT_DB)

engine = create_engine(
    DB_PATH,
    connect_args={"check_same_thread": False} if DB_PATH.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
