import polars as pl
import os

dirname = os.path.dirname(__file__)
data_dir = os.path.join(os.path.dirname(os.path.dirname((__file__))), "datasets")
team_stats_dir = os.path.join(data_dir, "team_stats.csv")
print(team_stats_dir)

def teams():
    df = pl.read_csv(team_stats_dir)
    teams_df = df.select(pl.col("team")).unique().sort("team").to_dicts()
    teams = {"teams" : [team["team"] for team in teams_df]}
    return teams


    # get all teams from specific season
def teams_from_season(season: str):
    df = pl.read_csv(team_stats_dir)
    season_df = df.filter(pl.col("season") == season)
    teams_season_dict = season_df.select(pl.col("team")).unique().sort("team").to_dicts()
    teams = {f"{season}": [entry["team"] for entry in teams_season_dict]}
    return teams

    # get team stats for a specific team and season
def team_stats_from_season(team: str, season: str):
    team_stats_df = pl.read_csv(team_stats_dir)
    filtered_df = team_stats_df.filter((pl.col("team") == team) & (pl.col("season") == season))
    stats = filtered_df.drop("team").drop("season").to_dicts()
    return stats


    # get team stats from specific season for basic ranking table
def team_stats_for_table(season: str):
    df = pl.read_csv(team_stats_dir)
