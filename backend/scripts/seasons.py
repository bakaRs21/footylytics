import polars as pl
from pathlib import Path

    # Get base and data directories
base_dir = Path(__file__).resolve().parent.parent
data_dir = base_dir / "datasets"

    # Specific data file paths
team_stats_dir = data_dir / "team_stats.csv"
player_stats_dir = data_dir / "players_2006-2018.csv"


    # Get all unique seasons
def seasons():
    df = pl.read_csv(team_stats_dir)
    seasons_df = df.select(pl.col("season")).unique().sort("season").to_dicts()
    seasons = {"seasons" : [season["season"] for season in seasons_df]}
    return seasons

    # Get all season for specific team
def seasons_for_team(team: str):
    df = pl.read_csv(team_stats_dir)
    team_seasons_df = df.filter(pl.col("team") == team).select(pl.col("season")).unique().sort("season").to_dicts()
    team_seasons = {f"{team}_seasons": [season["season"] for season in team_seasons_df]}
    return team_seasons

# NEEDS FIXING - SHOULD RETURN OVERALL STATS FOR A SEASON WITHOUT TEAMS
def stats_for_season(season: str):
    df = pl.read_csv(team_stats_dir)
    season_stats_df = df.filter(pl.col("season") == season).to_dicts()
    return season_stats_df
