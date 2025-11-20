import polars as pl
from pathlib import Path

    # Get base and data directories
base_dir = Path(__file__).resolve().parent.parent.parent
data_dir = base_dir / "datasets"

    # Specific data file paths
player_stats_dir = data_dir / "players_2006-2018.csv"

def players():
    df = pl.read_csv(player_stats_dir)
    players_df = df.select(pl.col("name")).unique().sort("name").to_dicts()
    players = {"players" : [player["name"] for player in players_df]}
    return players

    # Get seasons for a specific player
def player_seasons(player: str):
    df = pl.read_csv(player_stats_dir)
    player_df = df.filter(pl.col("name") == player)
    player_season_dict = player_df.select(pl.col("name", "season")).unique().sort("season").to_dicts()
    seasons = [entry["season"] for entry in player_season_dict]
    player_season = {f"{player}": seasons}
    return player_season

    # get all players from specific season
def players_from_season(season: str):
    df = pl.read_csv(player_stats_dir)
    season_df = df.filter(pl.col("season") == season)
    players_season_dict = season_df.select(pl.col("name")).unique().sort("name").to_dicts()
    players = {f"players_{season}": [entry["name"] for entry in players_season_dict]}
    return players

    # Get player stats for a specific player and season
def player_stats_from_season(player: str, season: str):
    player_stats_df = pl.read_csv(player_stats_dir)
    filtered_df = player_stats_df.filter((pl.col("name") == player) & (pl.col("season") == season))
    stats = filtered_df.drop("name").drop("season").to_dicts()
    return stats
