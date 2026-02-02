import dotenv
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path
import os

base_path = Path(__file__).resolve().parent
dotenv.load_dotenv(base_path / ".env")

"""POSTGRES_USER = dotenv.get_key(base_path / ".env", "DB_USER")
POSTGRES_PASSWORD = dotenv.get_key(base_path / ".env", "DB_PASSWORD")
POSTGRES_HOST = dotenv.get_key(base_path / ".env", "DB_HOST")
POSTGRES_PORT = dotenv.get_key(base_path / ".env", "DB_PORT")
POSTGRES_DB = dotenv.get_key(base_path / ".env", "DB_NAME")"""
POSTGRES_USER = os.getenv("DB_USER")
POSTGRES_PASSWORD = os.getenv("DB_PASSWORD")
POSTGRES_HOST = os.getenv("DB_HOST")
POSTGRES_PORT = os.getenv("DB_PORT")
POSTGRES_DB = os.getenv("DB_NAME")
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata_obj = MetaData()

def get_session():
    return SessionLocal()

def get_selected_table(table_name: str):
    metadata_obj.clear()

    table = Table(table_name, metadata_obj, autoload_with=engine)
    return table