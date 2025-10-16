import polars as pl
from pathlib import Path
import os


def process_dataset():
    data = [1, 2, 3, 4, 5]
    processed_data = [x * 2 for x in data]
    return processed_data

def team_names():
    base_dir = Path(__file__).parent
    data_dir = base_dir / "datasets" / "players-for-team"
    teams = os.listdir(data_dir)[:39]
    teams = [team.replace(".csv", "").replace("-", " ") for team in teams]
    return teams