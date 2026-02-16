import dotenv
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path
import os

base_path = Path(__file__).resolve().parent
dotenv.load_dotenv(base_path / ".env")

POSTGRES_USER = os.getenv("DB_USER")
POSTGRES_PASSWORD = os.getenv("DB_PASSWORD")
POSTGRES_HOST = os.getenv("DB_HOST")
POSTGRES_PORT = os.getenv("DB_PORT")
POSTGRES_DB = os.getenv("DB_NAME")
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

print(f"DEBUG - DB_USER: {POSTGRES_USER}")
print(f"DEBUG - DB_HOST: {POSTGRES_HOST}")
print(f"DEBUG - DB_PORT: {POSTGRES_PORT}")
print(f"DEBUG - DB_NAME: {POSTGRES_DB}")
print(f"DEBUG - DATABASE_URL: {DATABASE_URL}")

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