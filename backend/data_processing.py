import polars as pl
from pathlib import Path
import os

base_dir = Path(__file__).parent
data_dir = base_dir / "datasets"

def process_dataset():
    data = [1, 2, 3, 4, 5]
    processed_data = [x * 2 for x in data]
    return processed_data

def team_names():
    team_dir = data_dir / "team_stats"
    teams = os.listdir(team_dir)[:39]
    teams = [team.replace(".csv", "").replace("_", " ") for team in teams]
    return teams

def seasons():
    season_dir = data_dir / "team_stats.csv"
    df = pl.read_csv(season_dir)
    seasons_df = df.select(pl.col("season")).unique().sort("season").to_dicts()
    seasons = {"seasons" : [season["season"] for season in seasons_df]}
    return seasons
