import asyncpg
import dotenv
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Optional
from pathlib import Path


base_path = Path(__file__).resolve().parent
dotenv.load_dotenv(base_path / ".env")

POSTGRES_USER = dotenv.get_key(base_path / ".env", "DB_USER")
POSTGRES_PASSWORD = dotenv.get_key(base_path / ".env", "DB_PASSWORD")
POSTGRES_HOST = dotenv.get_key(base_path / ".env", "DB_HOST")
POSTGRES_PORT = dotenv.get_key(base_path / ".env", "DB_PORT")
POSTGRES_DB = dotenv.get_key(base_path / ".env", "DB_NAME")
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata_obj = MetaData()

def get_session():
    return SessionLocal()

pool : Optional[asyncpg.pool.Pool] = None
"""
async def connect_db():
    global pool
    try:
        pool = await asyncpg.create_pool(min_size=1, max_size=10, dsn=DATABASE_URL)
    except Exception as e:
        print(f"Error creating database connection pool: {e}")
        raise
    print("Database connection pool created")

async def disconnect_db():
    global pool
    if pool:
        await pool.close()
        print("Database connection pool closed")

async def get_db():
    async with pool.acquire() as connection:
        yield connection
"""




def get_selected_table(table_name: str):
    metadata_obj.clear()

    table = Table(table_name, metadata_obj, autoload_with=engine)
    return table



