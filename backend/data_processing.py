import polars as pl
from pathlib import Path
import os

base_dir = Path(__file__).parent
data_dir = base_dir / "datasets"
team_stats_dir = data_dir / "team_stats.csv"
all_matches_dir = data_dir / "all_matches.csv"
all_players_dir = data_dir / "players_2006-2018.csv"
results_dir = data_dir / "results_2006-2018.csv"
top20_teams_players_dir = data_dir / "top20_teams_players_2006-18.csv"

def process_dataset():
    data = [1, 2, 3, 4, 5]
    processed_data = [x * 2 for x in data]
    return processed_data

def team_names():
    team_df = pl.read_csv(team_stats_dir)
    teams = team_df.select(pl.col("team").unique()).sort("team").to_dicts()
    return {"teams": [team["team"] for team in teams]}

print(team_names())
def team_seasons(team: str):
    df = pl.read_csv(team_stats_dir)
    team_df = df.filter(pl.col("team") == team)
    team_season_dict = team_df.select(pl.col("team", "season")).unique().sort("season").to_dicts()
    seasons = [entry["season"] for entry in team_season_dict]
    team_season = {f"{team}_seasons": seasons}
    return team_season

def team_stats_from_season(team: str, season: str):
    team_stats_df = pl.read_csv(team_stats_dir)
    filtered_df = team_stats_df.filter((pl.col("team") == team) & (pl.col("season") == season))
    stats = filtered_df.drop("team").drop("season").to_dicts()
    return stats



def seasons():
    season_dir = data_dir / "team_stats.csv"
    df = pl.read_csv(season_dir)
    seasons_df = df.select(pl.col("season")).unique().sort("season").to_dicts()
    seasons = {"seasons" : [season["season"] for season in seasons_df]}
    return seasons
