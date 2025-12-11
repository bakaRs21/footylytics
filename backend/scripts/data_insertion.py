import psycopg2
import polars as pl
import dotenv
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent

async def get_table_columns(conn, table_name: str):
    try:
        columns = await conn.fetch("SELECT column_name FROM information_schema.columns WHERE table_name = $1;", table_name)
        return [col["column_name"] for col in columns]
    except Exception as e:
        print(f"Error fetching columns for table {table_name}: {e}")

async def insert_to_db(file, selected_table, conn):

    #start with uploading teams, then players, referees

    # if all_matches -> match will be store by finding pk of these columns and writing them with all other columns
    # season_id = Column(Integer, ForeignKey("seasons.season_id"))
    # referee_id = Column(Integer, ForeignKey("referees.referee_id"))
    # home_team_id = Column(Integer, ForeignKey("teams.team_id"))
    # away_team_id = Column(Integer, ForeignKey("teams.team_id"))

    #if player -> if not exist insert matching columns, then find play_has_seasons and insert all other matching columns, these needs to have referenced pk (if they exist)
    # player_id = Column(Integer, ForeignKey("players.player_id"), primary_key=True)
    # season_id = Column(Integer, ForeignKey("seasons.season_id"), primary_key=True)
    # team_id = Column(Integer, ForeignKey("teams.team_id"))

    #if teams -> same process, go to team_has_season and insert all other matching columns with referenced pk | COLUMNS CHECKED
    # team_id = Column(Integer, ForeignKey("teams.team_id"), primary_key=True)
    # season_id = Column(Integer, ForeignKey("seasons.season_id"), primary_key=True)

    #first thing first open transaction
    async with conn.transaction():
        valid_columns = await get_table_columns(conn, selected_table)
        df_csv = pl.read_csv(file)
        if selected_table:
            return
        return








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