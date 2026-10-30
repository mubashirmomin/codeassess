from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://codeadmin:supersecretpassword@db:5432/codeassess"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 3. Create the session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Define Base (This is what models.py is looking for!)
Base = declarative_base()