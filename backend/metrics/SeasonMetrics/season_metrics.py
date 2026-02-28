from fastapi import APIRouter, Depends, HTTPException
from Database import get_session
from scripts.models_updated import Season
from sqlalchemy.orm import Session

router = APIRouter(prefix="/season-metrics", tags=["Season Metrics"])

router.get("/stats")
def get_season_stats(season_id: int, db: Session = Depends(get_session)):
    return "Season stats in progress..."