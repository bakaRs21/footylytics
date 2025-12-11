import polars as pl
from pathlib import Path
import os

    # Get base and data directories
dirname = os.path.dirname(__file__)
data_dir = os.path.join(os.path.dirname(os.path.dirname((__file__))), "datasets")
player_stats_dir = os.path.join(data_dir, "players_2006-2018.csv")


    #get all players
async def players(conn):
    rows = await conn.fetch("SELECT player_id, name FROM Players;")
    return dict(rows)

    # Get seasons for a specific player
async def player_seasons(player: str):
    df = pl.read_csv(player_stats_dir)
    player_df = df.filter(pl.col("name") == player)
    player_season_dict = player_df.select(pl.col("name", "season")).unique().sort("season").to_dicts()
    seasons = [entry["season"] for entry in player_season_dict]
    player_season = {f"{player}": seasons}
    return player_season

    # get all players from specific season
async def players_from_season(season: str):
    df = pl.read_csv(player_stats_dir)
    season_df = df.filter(pl.col("season") == season)
    players_season_dict = season_df.select(pl.col("name")).unique().sort("name").to_dicts()
    players = {f"players_{season}": [entry["name"] for entry in players_season_dict]}
    return players

    # Get player stats for a specific player and season
async def player_stats_from_season(player: str, season: str):
    player_stats_df = pl.read_csv(player_stats_dir)
    filtered_df = player_stats_df.filter((pl.col("name") == player) & (pl.col("season") == season))
    stats = filtered_df.drop("name").drop("season").to_dicts()
    return stats
