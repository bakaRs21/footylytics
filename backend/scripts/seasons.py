import polars as pl
from pathlib import Path

    # Get base and data directories
base_dir = Path(__file__).resolve().parent.parent
data_dir = base_dir / "datasets"

    # Specific data file paths
team_stats_dir = data_dir / "team_stats.csv"
player_stats_dir = data_dir / "players_2006-2018.csv"


    # Get all unique seasons
async def seasons(conn):
    try:
        row = await conn.fetch("SELECT season_id, season FROM seasons;")
        return dict(row)
    except Exception as e:
        print(f"Error fetching seasons: {e}")

    # Get all seasons for specific team
async def seasons_for_team(conn, team: str):
    row = await conn.fetch("SELECT ")

# NEEDS FIXING - SHOULD RETURN OVERALL STATS FOR A SEASON WITHOUT TEAMS
async def stats_for_season(conn,season: str):
    df = pl.read_csv(team_stats_dir)
    season_stats_df = df.filter(pl.col("season") == season).to_dicts()
    return season_stats_df
