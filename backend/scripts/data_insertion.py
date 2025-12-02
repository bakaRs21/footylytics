import psycopg2
import polars as pl
import dotenv
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
datasets_dir = base_dir / "datasets"

env_dir = base_dir / ".env"


def insert_to_db(file, selected_table):
    print(f"File {file}, selected_table: {selected_table}")












dbname = dotenv.get_key(env_dir, "DB_NAME")
user = dotenv.get_key(env_dir, "DB_USER")
password = dotenv.get_key(env_dir, "DB_PASSWORD")
host = dotenv.get_key(env_dir, "DB_HOST")
port = dotenv.get_key(env_dir, "DB_PORT")
db_url = dotenv.get_key(env_dir, "DATABASE_URL")

def script_start():
    print(f"Notice: This script was aborted, now you fastapi upload-csv endopoint to insert data into the DB")
    print(f"\nFirst thing's first\nPUT your CSV file INTO THIS directory --> {datasets_dir}\n")
    while True:
        try:
            input("After that press enter ........")
            return pick_csv_file()
        except KeyboardInterrupt:
            print("\nExiting script.")
            exit(0)

def pick_csv_file():
    print("Available CSV files: ")
    csv_files = list(datasets_dir.glob("*.csv"))
    i=0
    for i, file in enumerate(csv_files):
        print(f"{i}", file.name)

    while True:
        choice = int(input(f"Select one of the files 0-{i}: "))
        try:
            selected_file = csv_files[choice]
            print(f"You selected: {selected_file.name}")
            print(f"Selection complete, now connecting to DB.......")
            break
        except (IndexError, ValueError):
            print("Invalid selection. Please try again.")

    while True:
        try:
                connection = psycopg2.connect(
                    dbname=dbname,
                    user=user,
                    password=password,
                    host=host,
                    port=port
                )
                connection.cursor()
                print("Database connection established.")
                return insertion_to_db(selected_file)
        except psycopg2.OperationalError as e:
                print(f"Database connection failed: {e}. Retrying...")

def insertion_to_db(selected_file):
    print(f"Inserting data from {selected_file} into the database...")