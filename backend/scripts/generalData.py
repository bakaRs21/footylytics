import polars as pl
from pathlib import Path

    # Get base and data directories
base_dir = Path(__file__).resolve().parent.parent.parent
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
