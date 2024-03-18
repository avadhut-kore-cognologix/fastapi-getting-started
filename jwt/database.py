from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = "sqlite:///./sql.db"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()