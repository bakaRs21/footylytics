from typing import List, Optional
from scripts.models_updated import Team, TeamSeason, Season
from sqlalchemy.orm import Session

    #get all teams
def teams(session: Session) -> List[Team]:
    try:
        return session.query(Team).all()
    finally:
        session.close()

    #get a single team by ID
def get_team(team_id: int, session: Session) -> Optional[Team]:
    try:
        return session.query(Team).filter(Team.team_id == team_id).first()
    finally:
        session.close()

def team_info(team_id: int, session: Session) -> Optional[Team]:
    try:
        return session.query(Team).filter(Team.team_id == team_id).first()
    finally:
        session.close()

    # get all teams from specific season
async def teams_from_season(season_id: int, session: Session):
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

    # get seasons for a specific team
async def seasons_for_team(team_id: int, session: Session):
    try:
        seasons = (session.query(Season.season)
                .join(TeamSeason, TeamSeason.season_id == Season.season_id)
                .filter(TeamSeason.team_id == team_id)
                .all()
                )
        if not seasons:
            raise ValueError(f"Seasons for team with id {team_id} not found")
        flat_seasons = [s[0] for s in seasons]
        return flat_seasons
    finally:
        session.close()