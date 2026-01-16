from typing import Optional
from pathlib import Path
from Database import get_session
from scripts.models_updated import Season
from typing import List


    # Get all unique seasons
def seasons()-> List[Season]:
    session = get_session()
    try:
        return session.query(Season).all()
    finally:
        session.close()

    # Create season
def create_season(season: str) -> Season:
    session = get_session()
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
def get_season(season_id: int) -> Optional[Season]:
    session = get_session()
    try:
        return session.query(Season).filter(Season.season_id == season_id).first()
    finally:
        session.close()

