"""
Database connection setup.

Locally: defaults to SQLite, zero config needed.
On Render (or anywhere with Postgres): set the DATABASE_URL environment
variable to your Postgres connection string and this file picks it up
automatically — no code change required.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# On Vercel, the filesystem is read-only except for /tmp.
# If no Postgres URL is provided, fallback to an ephemeral SQLite DB in /tmp.
try:
    with open("./.test_write", "w") as f:
        f.write("test")
    os.remove("./.test_write")
    default_db = "sqlite:///./shielding.db"
except OSError:
    default_db = "sqlite:////tmp/shielding.db"

SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", default_db)

# Render's Postgres URLs sometimes start with "postgres://" — SQLAlchemy 2.x
# requires "postgresql://". Normalize it so deployment doesn't silently break.
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


_db_initialized = False

def init_db():
    global _db_initialized
    if _db_initialized:
        return
        
    Base.metadata.create_all(bind=engine)
    
    try:
        import seed as seed_basic_module
        import seed_50 as seed_50_module
        seed_basic_module.seed()
        seed_50_module.seed()
    except Exception as e:
        print(f"[lazy seeding] skipped due to error: {e}")
        
    _db_initialized = True


def get_db():
    """FastAPI dependency — yields a DB session per-request, closes it after."""
    init_db()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
