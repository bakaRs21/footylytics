from typing import List, Optional
from scripts.models_updated import Referee, Match
from sqlalchemy.orm import Session, joinedload

def get_referees(session: Session) -> List[Referee]:
    try:
        return session.query(Referee).all()
    finally:
        session.close()