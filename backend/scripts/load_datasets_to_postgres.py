#!/usr/bin/env python3
"""
Load CSVs from backend/datasets into PostgreSQL.

Usage:
  - Create backend/.env with DATABASE_URL or DB_USER/DB_PASSWORD/DB_HOST/DB_PORT/DB_NAME (see .env.example).
  - Start Postgres (docker compose suggested).
  - pip install pandas sqlalchemy psycopg2-binary python-dotenv
  - python backend/scripts/load_datasets_to_postgres.py

What it does:
  - runs the SQL create_tables file
  - loads results_2006-2018.csv into results (typed)
  - loads all_matches_2006-2018.csv into all_matches (tries to map columns, else keeps others in metadata)
  - loads team_stats.csv into team_stats_raw (row -> jsonb)
  - loads players_2006-2018.csv and top20_teams_players_2006-18.csv into players_raw/top20_players_raw (row -> jsonb)
  - normalizes EPLStandings.csv into epl_standings (team, season, position)
"""

import os
import pathlib
import json
import tempfile
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

HERE = pathlib.Path(__file__).resolve().parents[1]  # backend/
load_dotenv(HERE / ".env")  # safe if file present

# Build DATABASE_URL if not provided
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    user = os.getenv("DB_USER", "pluser")
    pw = os.getenv("DB_PASSWORD", "plpass")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    db = os.getenv("DB_NAME", "premier_league")
    DATABASE_URL = f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}"

print("Using DB URL:", DATABASE_URL)
engine = create_engine(DATABASE_URL)

datasets_dir = HERE / "datasets"
if not datasets_dir.exists():
    raise SystemExit(f"datasets directory not found: {datasets_dir}")

# Run SQL to create tables
sql_path = HERE / "sql" / "create_tables.sql"
if sql_path.exists():
    print("Running schema SQL:", sql_path)
    with sql_path.open("r", encoding="utf-8") as f:
        sql = f.read()
    with engine.begin() as conn:
        conn.execute(text(sql))
else:
    print("Schema SQL not found at", sql_path, "- continuing (loader will create tables if needed)")

def df_row_to_jsonb_series(df_row):
    # Convert pandas Series to JSON-serializable dict, mapping NaN -> None
    d = {}
    for k, v in df_row.items():
        if pd.isna(v):
            d[k] = None
        else:
            # If numpy types, convert to native
            try:
                json.dumps(v)
                d[k] = v
            except TypeError:
                d[k] = str(v)
    return d

# 1) Load results_2006-2018.csv into results
results_path = datasets_dir / "results_2006-2018.csv"
if results_path.exists():
    print("Loading results:", results_path)
    df = pd.read_csv(results_path)
    # Clean column dtypes
    df = df.rename(columns=lambda c: c.strip())
    # coerce goals to int where possible
    for c in ("home_goals", "away_goals"):
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")
    # write to SQL
    df.to_sql("results", engine, index=False, if_exists="append", method="multi", chunksize=2000)
    print("  results rows written:", len(df))
else:
    print("results file not found:", results_path)

# 2) Load all_matches_2006-2018.csv into all_matches (try to map some columns)
all_matches_path = datasets_dir / "all_matches_2006-2018.csv"
if all_matches_path.exists():
    print("Loading all_matches:", all_matches_path)
    df = pd.read_csv(all_matches_path)
    df = df.rename(columns=lambda c: c.strip())
    # Prepare rows for insertion: try to extract common columns then put rest into metadata
    expected_cols = {"match_date", "home_team", "away_team", "home_goals", "away_goals", "season"}
    rows = []
    for _, r in df.iterrows():
        row = {}
        metadata = {}
        for col, val in r.items():
            if pd.isna(val):
                v = None
            else:
                v = val
            if col in expected_cols:
                row[col] = v
            else:
                metadata[col] = v
        row["metadata"] = json.dumps(metadata) if metadata else None
        rows.append(row)
    # Use pandas DataFrame to write quickly
    df_rows = pd.DataFrame(rows)
    # coerce goals
    for c in ("home_goals", "away_goals"):
        if c in df_rows.columns:
            df_rows[c] = pd.to_numeric(df_rows[c], errors="coerce").astype("Int64")
    df_rows.to_sql("all_matches", engine, index=False, if_exists="append", method="multi", chunksize=2000)
    print("  all_matches rows written:", len(df_rows))
else:
    print("all_matches file not found:", all_matches_path)

# 3) Load team_stats.csv into team_stats_raw as JSONB
team_stats_path = datasets_dir / "team_stats.csv"
if team_stats_path.exists():
    print("Loading team_stats:", team_stats_path)
    df = pd.read_csv(team_stats_path)
    df = df.rename(columns=lambda c: c.strip())
    rows = []
    for _, r in df.iterrows():
        d = df_row_to_jsonb_series(r)
        # keep team separate if present
        team = d.pop("team", None)
        rows.append({"team": team, "stats": json.dumps(d)})
    pd.DataFrame(rows).to_sql("team_stats_raw", engine, index=False, if_exists="append", method="multi", chunksize=2000)
    print("  team_stats rows written:", len(rows))
else:
    print("team_stats file not found:", team_stats_path)

# 4) Load players_2006-2018.csv and top20_teams_players_2006-18.csv into players_raw / top20_players_raw as JSONB
for name in ("players_2006-2018.csv", "top20_teams_players_2006-18.csv"):
    p = datasets_dir / name
    table = "players_raw" if "players_2006-2018" in name else "top20_players_raw"
    if p.exists():
        print("Loading", name, "->", table)
        df = pd.read_csv(p)
        df = df.rename(columns=lambda c: c.strip())
        rows = []
        for _, r in df.iterrows():
            rows.append({"raw": json.dumps(df_row_to_jsonb_series(r))})
        pd.DataFrame(rows).to_sql(table, engine, index=False, if_exists="append", method="multi", chunksize=1000)
        print("  rows written:", len(rows))
    else:
        print("  not found:", p)

# 5) Normalize EPLStandings.csv (wide -> tall) to epl_standings
epl_path = datasets_dir / "EPLStandings.csv"
if epl_path.exists():
    print("Loading EPLStandings:", epl_path)
    df = pd.read_csv(epl_path)
    df = df.rename(columns=lambda c: c.strip())
    # Columns: Team, years...
    team_col = "Team"
    years = [c for c in df.columns if c != team_col]
    rows = []
    for _, r in df.iterrows():
        team = r[team_col]
        for yr in years:
            pos = r.get(yr)
            if pd.isna(pos):
                continue
            try:
                pos_int = int(pos)
            except Exception:
                # if value cannot be cast, skip
                continue
            rows.append({"team": team, "season": str(yr), "position": pos_int})
    if rows:
        pd.DataFrame(rows).to_sql("epl_standings", engine, index=False, if_exists="append", method="multi", chunksize=1000)
        print("  epl_standings rows written:", len(rows))
    else:
        print("  no epl rows to write")
else:
    print("EPLStandings file not found:", epl_path)

print("Done.")