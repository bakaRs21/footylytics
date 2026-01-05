from typing import Optional
import polars as pl
from pathlib import Path
from Database import get_session
from scripts.models_updated import Seasons
from typing import List

    # Get base and data directories
base_dir = Path(__file__).resolve().parent.parent
data_dir = base_dir / "datasets"

    # Specific data file paths
team_stats_dir = data_dir / "team_stats_with_standing.csv"
player_stats_dir = data_dir / "players_2006-2018.csv"


    # Get all unique seasons
async def seasons(limit: int = 50) -> List[Seasons]:
    df = pl.read_csv(team_stats_dir)
    seasons_df = df.select(pl.col("season")).unique().sort("season").to_dicts()
    print(seasons_df)
    seasons = {"seasons" : [season["season"] for season in seasons_df]}
    return seasons
    session = get_session()
    try:
        return session.query(Seasons).limit(limit).all()
    finally:
        session.close()

    # Create season
def create_season(season: str) -> Seasons:
    session = get_session()
    try:
        s = Seasons(season=season)
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
def get_season(season_id: int) -> Optional[Seasons]:
    session = get_session()
    try:
        return session.query(Seasons).filter(Seasons.season_id == season_id).first()
    finally:
        session.close()

    # Get all seasons for specific team
async def seasons_for_team(team: str):
    df = pl.read_csv(team_stats_dir)
    team_seasons_df = df.filter(pl.col("name") == team).select(pl.col("season")).unique().sort("season").to_dicts()
    print(f"team_seasons_df: {team_seasons_df}")
    team_seasons = {f"{team}_seasons": [season["season"] for season in team_seasons_df]}
    return team_seasons

# NEEDS FIXING - SHOULD RETURN OVERALL STATS FOR A SEASON WITHOUT TEAMS
async def stats_for_season(season: str):
    df = pl.read_csv(team_stats_dir)
    season_stats_df = df.filter(pl.col("season") == season).to_dicts()
    return season_stats_df
