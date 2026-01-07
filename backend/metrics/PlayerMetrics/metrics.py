from fastapi import APIRouter, Depends, Query
from requests import Session
from Database import get_session
from scripts.models_updated import Player, PlayerSeason
from sqlalchemy import func
from typing import Optional

router = APIRouter(prefix="/player-metrics", tags=["Player Metrics"])

metric_options = [
    {
        "key": 'player_goals_per_match',
        "label": "Player Average Goals per Match",
        "params": [
            {"name": "player_id", 'type': 'int', 'required': False, 'help': 'Filter to one player_id; if skipped return all players'},
            {'name': 'season_id', 'type': 'int', 'required': False, 'help': 'Filter to one season_id; if skipped return all seasons'},
        ]
    }, {
        "key": 'player_assists_per_match',
        "label": "Player Average Assists per Match",
        "params": [
            {"name": "player_id", 'type': 'int', 'required': False, 'help': 'Filter to one player_id; if skipped return all players'},
            {'name': 'season_id', 'type': 'int', 'required': False, 'help': 'Filter to one season_id; if skipped return all seasons'},
        ]
    }, {
        "key": 'player_shots_per_match',
        "label": "Player Average Shots per Match",
        "params": [
            {"name": "player_id", 'type': 'int', 'required': False, 'help': 'Filter to one player_id; if skipped return all players'},
            {'name': 'season_id', 'type': 'int', 'required': False, 'help': 'Filter to one season_id; if skipped return all seasons'},
        ]
    },
]

@router.get("/options")
def get_metric_options():
    return metric_options

def player_queries(db: Session, player_id: int | None, season_id: int | None):
    query = db.query(
        Player.player_id,
        Player.name,
        func.count().label("games_appearences"),
        func.sum(PlayerSeason.games_appearences).label("total_games_appearences"),
        func.sum(PlayerSeason.games_minutes).label("total_minutes_played"),
        func.sum(PlayerSeason.goals_total).label("total_goals"),
        func.sum(PlayerSeason.shots_total).label("total_shots")
    )

    query = query.join(PlayerSeason, Player.player_id == PlayerSeason.player_id)

    if player_id is not None:
        query = query.filter(PlayerSeason.player_id == player_id)
    if season_id is not None:
        query = query.filter(PlayerSeason.season_id == season_id)

    query = query.group_by(Player.player_id, Player.name
    ).having(func.sum(PlayerSeason.games_appearences) > 0
    ).order_by(func.sum(PlayerSeason.goals_total).desc())

    return query.all()

@router.get("/player-goals-per-match")
def player_goals_per_match(
    player_id: int | None = Query(None, description="Filter to one player_id; if skipped return all players"),
    season_id: int | None = Query(None, description="Filter to one season_id; if skipped return all seasons"),
    db: Session = Depends(get_session)
    ):
    rows = player_queries(db, player_id, season_id)
    return [
        {
            "player_id": r.player_id,
            "player_name": r.name,
            "player_total_goals": r.total_goals,
            "player_total_game_appearences": r.total_games_appearences,
            "average_goals_per_match": ((r.total_goals or 0) / r.total_games_appearences) if r.total_games_appearences or 0 > 0 else 0
        }
        for r in rows
    ]