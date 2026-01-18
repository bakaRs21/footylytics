import pandas as pl
from Database import get_session
from typing import List, Optional
from scripts.models_updated import Team, TeamSeason, Season

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
async def teams_from_season(season_id: int):
    session = get_session()
    try:
        teams = (session.query(Team.name)
                .join(TeamSeason, TeamSeason.team_id == Team.team_id)
                .join(Season, Season.season_id == TeamSeason.season_id)
                .filter(Season.season_id == season_id)
                .all()
                )
        if not teams:
            raise ValueError(f"Teams for season with id {season_id} not found")
        return teams
    finally:
        session.close()

async def seasons_for_team(team_id: int):
    session = get_session()
    try:
        seasons = (session.query(Season.season)
                .join(TeamSeason, TeamSeason.season_id == Season.season_id)
                .join(Team, Team.team_id == TeamSeason.team_id)
                .filter(Team.team_id == team_id)
                .all()
                )
        if not seasons:
            raise ValueError(f"Seasons for team with id {team_id} not found")
        return [row[0] for row in seasons]
    finally:
        session.close()

    # get team stats for a specific team and season
async def team_stats_from_season(team_id: int, season_id: int):
    session = get_session()
    try:
        return
    finally:
        session.close()


