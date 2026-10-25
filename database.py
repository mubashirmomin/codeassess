from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Use SQLite for local testing until Docker is installed
SQLALCHEMY_DATABASE_URL = "sqlite:///./codeassess.db"

# 2. Create the SQLite engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create the session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Define Base (This is what models.py is looking for!)
Base = declarative_base()