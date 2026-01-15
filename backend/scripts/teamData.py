import pandas as pl
from Database import get_session
from typing import List, Optional
from scripts.models_updated import Team, TeamSeason, Season
import os

    #get all teams
def teams(limit: int = 50) -> List[Team]:
    session = get_session()
    try:
        return session.query(Team).all()
    finally:
        session.close()

    #get a single team by ID
def get_team(team_id: int) -> Optional[Team]:
    session = get_session()
    try:
        return session.query(Team).filter(Team.team_id == team_id).first()
    finally:
        session.close()

def team_info(team_id: int) -> Optional[Team]:
    session = get_session()
    try:
        return session.query(Team).filter(Team.team_id == team_id).first()
    finally:
        session.close()

    # get all teams from specific season
def teams_from_season(season_id: int):
    session = get_session()
    try:
        return session.query()
    finally:
        session.close()

    # get team stats for a specific team and season
def team_stats_from_season(team_id, season_id):
    session = get_session()
    try:
        return
    finally:
        session.close()


