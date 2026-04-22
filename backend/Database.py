from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_USER = os.environ.get("DB_USER")
POSTGRES_PASSWORD = os.environ.get("DB_PASSWORD")
POSTGRES_HOST = os.environ.get("DB_HOST")
POSTGRES_PORT = os.environ.get("DB_PORT")
POSTGRES_DB = os.environ.get("DB_NAME")
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata_obj = MetaData()

def get_session():
    db =  SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_selected_table(table_name: str):
    metadata_obj.clear()

    table = Table(table_name, metadata_obj, autoload_with=engine)
    return table