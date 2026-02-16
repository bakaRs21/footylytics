from fastapi import APIRouter, Depends, Query
from requests import Session
from Database import get_session
from scripts.models_updated import Player, PlayerSeason
from sqlalchemy import func

router = APIRouter(prefix="/player-metrics", tags=["Player Metrics"])

METRIC_MAP = {
    "goals_per_match": {
        "primary_column": PlayerSeason.goals_total,
        "additional_column": [PlayerSeason.games_appearences],
        "label_map": {
            "primary": "total_goals",
            "additional": ["total_game_appearances"]
        }
    }, "assists_per_match": {
        "primary_column": PlayerSeason.goals_assists,
        "additional_column": [PlayerSeason.games_appearences],
        "label_map": {
            "primary": "total_assists",
            "additional": ["total_game_appearances"]
        }
    }, "shots_per_match": {
        "primary_column": PlayerSeason.shots_total,
        "additional_column": [PlayerSeason.games_appearences],
        "label_map": {
            "primary": "total_shots",
            "additional": ["total_game_appearances"]
        }
    }, "minutes_per_match": {
        "primary_column": PlayerSeason.games_minutes,
        "additional_column": [PlayerSeason.games_appearences],
        "label_map": {
            "primary": "total_goals",
            "additional": ["total_game_appearances"]
        }
    }, "penalty_succes_rate": {
        "primary_column": PlayerSeason.penalty_scored,
        "additional_column": [PlayerSeason.penalty_missed],
        "label_map": {
            "primary": "penalties_scored",
            "additional": ["penalties_missed"]
        }
    }, "shots_accuracy": {
        "primary_column": PlayerSeason.shots_total,
        "additional_column": [PlayerSeason.shots_on],
        "label_map": {
            "primary": "total_shots",
            "additional": ["shots_on_goal"]
        }
    }
}

def player_queries(db: Session, player_id: int | None, season_id: int | None, metric_key: str):
    if metric_key not in METRIC_MAP:
        raise ValueError(f"Unsupported metric key: {metric_key}")
    mapped_key = METRIC_MAP[metric_key]
    query_cols = [
        Player.player_id,
        Player.name,
        func.sum(mapped_key["primary_column"].label(mapped_key["label_map"]["primary"]))
    ]
    for i, col in enumerate(mapped_key["additional_column"]):
        label = mapped_key["label_map"]["additional"][i]
        query_cols.append(func.sum(col).label(label))

    query = db.query(*query_cols).join(PlayerSeason, PlayerSeason.player_id == Player.player_id)

    if player_id is not None:
        query = query.filter(PlayerSeason.player_id == player_id)
    if season_id is not None:
        query = query.filter(PlayerSeason.season_id == season_id)

    query = query.group_by(Player.player_id, Player.name
    ).having(func.sum(mapped_key["additional_column"][0]) > 0
    ).order_by(func.sum(mapped_key["primary_column"]).desc())

    return query.all()

def get_basic_player_stats(db: Session, player_id: int | None = None, season_id: int | None = None):
    if season_id:
        player_season = (
            db.query(PlayerSeason)
            .filter(PlayerSeason.player_id == player_id, PlayerSeason.season_id == season_id)
            .first()
        )

        if not player_season:
            return None

        return {
            "player_id": player_id,
            "season_id": season_id,
            "market_value": player_season.market_value,
            "position": player_season.position,
            "total_matches_played": player_season.games_appearences,
            "total_minutes_played": player_season.games_minutes,
            "rating": player_season.games_rating,
            "total_shots": player_season.total_shots,
            "total_goals": player_season.goals_total,

        }

    else:
        player_seasons = (
            ddb.query(PlayerSeason)
            .filter(PlayerSeason.player_id == player_id)
            .all()
        )

        if not player_seasons:
            return None

        stats = {
            "player_id": player_id,
            "season_id": None,
            "total_seasons": len(player_seasons)
        }

@router.get("/goals-per-match")
def player_goals_per_match(
    player_id: int | None = Query(None, description="Filter to one player_id; if skipped return all players"),
    season_id: int | None = Query(None, description="Filter to one season_id; if skipped return all seasons"),
    db: Session = Depends(get_session)
    ):
    rows = player_queries(db, player_id, season_id, "goals_per_match")
    return [
        {
            "player_id": r.player_id,
            "player_name": r.name,
            "player_total_goals": r.total_goals,
            "player_total_game_appearences": r.total_games_appearences,
            "average_goals_per_match": round((r.total_goals or 0) / r.total_games_appearences, 3) if r.total_games_appearences or 0 > 0 else 0
        }
        for r in rows
    ]

@router.get("/shots-per-match")
def player_shots_per_match(
    player_id: int | None = Query(None, description="Filter to one player_id; if skipped return all players"),
    season_id: int | None = Query(None, description="Filter to one season_id; if skipped return all seasons"),
    db: Session = Depends(get_session)
    ):
    rows = player_queries(db, player_id, season_id, "shots_per_match")
    return [
        {
            "player_id": r.player_id,
            "player_name": r.name,
            "player_total_shots": r.total_shots,
            "player_total_game_appearences": r.total_games_appearences,
            "average_shots_per_match": round((r.total_shots or 0) / r.total_games_appearences, 3) if r.total_games_appearences or 0 > 0 else 0
        }
        for r in rows
    ]

@router.get("/assists-per-match")
def player_assists_per_match(
    player_id: int | None = Query(None, description="Filter to one player_id; if skipped return all players"),
    season_id: int | None = Query(None, description="Filter to one season_id; if skipped return all seasons"),
    db: Session = Depends(get_session)
    ):
    rows = player_queries(db, player_id, season_id, "assists_per_match")
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
    rows = player_queries(db, player_id, season_id, "minutes_per_match")
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
    rows = player_queries(db, player_id, season_id, "penalty_succes_rate")

    return [
        {
            "player_id": r.player_id,
            "player_name": r.name,
            "penalties_scored": r.penalties_scored,
            "penalties_missed": r.penalties_missed,
            "total_penalties": (r.penalties_scored) + (r.penalties_missed),
            "penalty_succes_rate": round(((r.penalties_scored) / ((r.penalties_scored) + (r.penalties_missed))) * 100, 3
            ) if (r.penalties_scored or 0) + (r.penalties_missed or 0) > 0 else 0
        }
        for r in rows
    ] 

@router.get("/shots-accuracy")
def player_shots_accuracy(
    player_id: int | None = Query(None, description="Filter to one player_id; if skipped return all players"),
    season_id: int | None = Query(None, description="Filter to one season_id; if skipped return all seasons"),
    db: Session = Depends(get_session)
    ):
    rows = player_queries(db, player_id, season_id, "shots_accuracy")

    return [
        {
            "player_id": r.player_id,
            "player_name": r.name,
            "total_shots": r.total_shots,
            "shots_on_target": r.shots_on_target,
            "accuracy_pct": round(((r.shots_on_target or 0) / (r.total_shots or 1)) * 100, 2
            ) if r.total_shots and r.total_shots > 0 else 0
        }
        for r in rows
    ]

@router.get("/basic-stats")
def basic_player_stats(
    player_id: int | None = None,
    season_id: int | None = None,
    db: Session = Depends(get_session)
):
    stats = get_basic_player_stats(db, player_id, season_id)
    if not stats:
        raise HTTPException(
            status_code=400,
            detail=f"No data found for team_id: {team_id}" + (f" and season_id: {season_id}" if season_id else "")
        )

    return stats