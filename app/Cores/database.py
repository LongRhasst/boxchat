from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.Cores.config import DATABASE_URL

engine = create_engine(DATABASE_URL)  # Không cần connect_args với MySQL

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
