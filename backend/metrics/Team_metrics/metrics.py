from fastapi import APIRouter
from Database import get_session

router = APIRouter(prefix="/metrics", tags=["metrics"])

metric_options = [
    {
        "key": 'team_goals_per_match',
        "label": "Team Avarage Goals per Match",
        "params": [
            {"name": "team_id", 'tpye': 'int', 'required': False, 'help': 'Filter to one team_id; if skipped return all teams'},
            {'name': 'season_id', 'type': 'int', 'required': False, 'help': 'Filter to one season_id; if skipped return all seasons'},
        ]
    },
]

@router.get("/options")
def get_metric_options():
    return metric_options

def get_db():
    with get_session() as db:
        yield db

@router.get("/team-goals-per-match")
def team_goals_per_match(team_id: int | None = None, season_id: int | None = None):