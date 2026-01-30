from fastapi import APIRouter, Depends, Query
from requests import Session
from Database import get_session
from scripts.models_updated import Player, PlayerSeason
from sqlalchemy import func

router = APIRouter(prefix="/player-metrics", tags=["Player Metrics"])


def player_match_queries(db: Session, player_id: int | None, season_id: int | None, metric_key: str):
    metric_map = {
        "goals_per_match": PlayerSeason.goals_total,
        "assists_per_match": PlayerSeason.goals_assists,
        "shots_per_match": PlayerSeason.shots_total,
        "minutes_per_match": PlayerSeason.games_minutes,
    }
    metric_column = metric_map.get(metric_key)
    if metric_column is None:
        raise ValueError(f"Unsupported metric key: {metric_key}")
    query = db.query(
        Player.player_id,
        Player.name,
        func.sum(PlayerSeason.games_appearences).label("total_games_appearences"),
        func.sum(metric_column).label(f"total_{metric_key.split('_per_')[0]}"),
    ).join(PlayerSeason, Player.player_id == PlayerSeason.player_id)

    if player_id is not None:
        query = query.filter(PlayerSeason.player_id == player_id)
    if season_id is not None:
        query = query.filter(PlayerSeason.season_id == season_id)

    query = query.group_by(Player.player_id, Player.name
    ).having(func.sum(PlayerSeason.games_appearences) > 0
    ).order_by(func.sum(PlayerSeason.goals_total).desc())

    return query.all()

@router.get("/goals-per-match")
def player_goals_per_match(
    player_id: int | None = Query(None, description="Filter to one player_id; if skipped return all players"),
    season_id: int | None = Query(None, description="Filter to one season_id; if skipped return all seasons"),
    db: Session = Depends(get_session)
    ):
    rows = player_match_queries(db, player_id, season_id, "goals_per_match")
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

@router.get("/shots-per-match")
def player_shots_per_match(
    player_id: int | None = Query(None, description="Filter to one player_id; if skipped return all players"),
    season_id: int | None = Query(None, description="Filter to one season_id; if skipped return all seasons"),
    db: Session = Depends(get_session)
    ):
    rows = player_match_queries(db, player_id, season_id, "shots_per_match")
    return [
        {
            "player_id": r.player_id,
            "player_name": r.name,
            "player_total_shots": r.total_shots,
            "player_total_game_appearences": r.total_games_appearences,
            "average_shots_per_match": ((r.total_shots or 0) / r.total_games_appearences) if r.total_games_appearences or 0 > 0 else 0
        }
        for r in rows
    ]

@router.get("/assists-per-match")
def player_assists_per_match(
    player_id: int | None = Query(None, description="Filter to one player_id; if skipped return all players"),
    season_id: int | None = Query(None, description="Filter to one season_id; if skipped return all seasons"),
    db: Session = Depends(get_session)
    ):
    rows = player_match_queries(db, player_id, season_id, "assists_per_match")
    return [
        {
            "player_id": r.player_id,
            "player_name": r.name,
            "player_total_assists": r.total_assists,
            "player_total_game_appearences": r.total_games_appearences,
            "average_assists_per_match": ((r.total_assists or 0) / r.total_games_appearences) if r.total_games_appearences or 0 > 0 else 0
        }
        for r in rows
    ]

@router.get("/minutes-per-match")
def minutes_per_match(
    player_id: int | None = Query(None, description="Filter to one player_id; if skipped return all players"),
    season_id: int | None = Query(None, description="Filter to one season_id; if skipped return all seasons"),
    db: Session = Depends(get_session)
    ):
    rows = player_match_queries(db, player_id, season_id, "minutes_per_match")
    return [
        {
            "payer_id": r.player_id,
            "player_name": r.name,
            "player_total_minutes": r.total_minutes,
            "player_total_game_appearences": r.total_games_appearences,
            "average_minutes_per_match": ((r.total_minutes or 0) / r.total_games_appearences) if r.total_games_appearences or 0 > 0 else 0
        }
        for r in rows
    ]


@router.get("/penalty-success-rate")
def player_penalty_success_rate(
    player_id: int | None = Query(None, description="Filter to one player_id; if skipped return all players"),
    season_id: int | None = Query(None, description="Filter to one season_id; if skipped return all seasons"),
    db: Session = Depends(get_session)
    ):
    rows = player_match_queries(db, player_id, season_id, "penalty_success_rate")
    return 