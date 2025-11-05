import polars as pl
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent.parent
data_dir = base_dir / "datasets"
team_stats_dir = data_dir / "team_stats.csv"

def teams():
    df = pl.read_csv(team_stats_dir)
    teams_df = df.select(pl.col("team")).unique().sort("team").to_dicts()
    teams = {"teams" : [team["team"] for team in teams_df]}
    return teams

    # Get seasons for a specific team
def team_seasons(team: str):
    df = pl.read_csv(team_stats_dir)
    team_df = df.filter(pl.col("team") == team)
    team_season_dict = team_df.select(pl.col("team", "season")).unique().sort("season").to_dicts()
    seasons = [entry["season"] for entry in team_season_dict]
    team_season = {f"{team}_seasons": seasons}
    return team_season

    # get all teams from specific season
def teams_from_season(season: str):
    df = pl.read_csv(team_stats_dir)
    season_df = df.filter(pl.col("season") == season)
    teams_season_dict = season_df.select(pl.col("team")).unique().sort("team").to_dicts()
    teams = {f"{season}": [entry["team"] for entry in teams_season_dict]}
    return teams

    # Get team stats for a specific team and season
def team_stats_from_season(team: str, season: str):
    team_stats_df = pl.read_csv(team_stats_dir)
    filtered_df = team_stats_df.filter((pl.col("team") == team) & (pl.col("season") == season))
    stats = filtered_df.drop("team").drop("season").to_dicts()
    return stats
