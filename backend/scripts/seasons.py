from typing import Optional
from scripts.models_updated import Season
from typing import List
from sqlalchemy.orm import Session


    # Get all unique seasons
def seasons(session: Session) -> List[Season]:
    try:
        return session.query(Season).all()
    finally:
        session.close()

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

