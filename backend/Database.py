import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

database_url = dotenv.get_key(".env", "DATABASE_URL")
engine = create_engine(database_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()