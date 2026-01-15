from typing import Optional
import polars as pl
from pathlib import Path
from Database import get_session
from scripts.models_updated import Season
from typing import List

    # Get base and data directories
base_dir = Path(__file__).resolve().parent.parent
data_dir = base_dir / "datasets"

    # Specific data file paths
team_stats_dir = data_dir / "team_stats_with_standing.csv"
player_stats_dir = data_dir / "players_2006-2018.csv"


    # Get all unique seasons
def seasons()-> List[Season]:
    session = get_session()
    try:
        return session.query(Season).all()
    finally:
        session.close()

    # Create season
def create_season(season: str) -> Season:
    session = get_session()
    try:
        s = Season(season=season)
        session.add(s)
        session.commit()
        session.refresh(s)
        return s
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


    #get a single season by ID
def get_season(season_id: int) -> Optional[Season]:
    session = get_session()
    try:
        return session.query(Season).filter(Season.season_id == season_id).first()
    finally:
        session.close()

    # get team for a season

# NEEDS FIXING - SHOULD RETURN OVERALL STATS FOR A SEASON WITHOUT TEAMS
def stats_for_season(season: str):
    df = pl.read_csv(team_stats_dir)
    season_stats_df = df.filter(pl.col("season") == season).to_dicts()
    return season_stats_df
