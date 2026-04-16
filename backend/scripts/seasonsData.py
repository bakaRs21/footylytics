from typing import Optional
from scripts.models_updated import Season, Match
from typing import List
from sqlalchemy.orm import Session


    # Get all unique seasons
def seasons(session: Session) -> List[Season]:
    try:
        seasons = session.query(Season).all()
    finally:
        session.close()
    return [
        {
            "season_id": s.season_id,
            "season": f"{s.season}-{int(s.season) + 1}"
        }
        for s in seasons
    ]
    # Create season
def create_season(season: str, session: Session) -> Season:
    try:
        s = Season(season=season)
        session.add(s)
        session.commit()
        session.refresh(s)
        return s
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


    #get a single season by ID
def get_season(season_id: int, session: Session) -> Optional[Season]:
    try:
        return session.query(Season).filter(Season.season_id == season_id).first()
    finally:
        session.close()

def get_matches_in_season(season_id: int, session: Session):
    try:
        matches = session.query(Match).filter(Match.season_id == season_id).all()
        if not matches:
            raise ValueError(f"Matches for season with id {season_id} not found")
        return matches
    finally:
        session.close()