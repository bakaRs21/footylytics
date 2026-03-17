from fastapi import APIRouter, Depends, HTTPException, Query
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
            "primary": "total_minutes",
            "additional": ["total_game_appearances"]
        }
    }, "penalty_success_rate": {
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
        func.sum(mapped_key["primary_column"]).label(mapped_key["label_map"]["primary"])
    ]
    if not query_cols:
        raise ValueError(f"No primary column defined for metric key: {metric_key}")
    for i, col in enumerate(mapped_key["additional_column"]):
        label = mapped_key["label_map"]["additional"][i]
        query_cols.append(func.sum(col).label(label))

    query = db.query(*query_cols).join(PlayerSeason, PlayerSeason.player_id == Player.player_id)
    if not query:
        raise ValueError("Query construction failed, no columns fetched")
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
            "team_id": player_season.team_id,
            "total_matches_played": player_season.games_appearences or 0,
            "total_minutes_played": player_season.games_minutes or 0,
            "rating": round(player_season.games_rating, 1) if player_season.games_rating is not None else None,
            "total_goals": player_season.goals_total or 0,
            "total_assists": player_season.goals_assists or 0,
            "total_shots": player_season.shots_total or 0,
            "shots_on_target": player_season.shots_on or 0,
            "total_tackles": player_season.tackles_total or 0,
            "tackles_blocks": player_season.tackles_blocks or 0,
            "tackles_interceptions": player_season.tackles_interceptions or 0,
            "total_passes": player_season.passes_total or 0,
            "key_passes": player_season.passes_key or 0,
            "total_duels": player_season.duels_total or 0,
            "duels_won": player_season.duels_won or 0,
            "dribbles_success": player_season.dribbles_success or 0,
            "dribbles_attempts": player_season.dribbles_attempts or 0,
            "yellow_cards": player_season.cards_yellow or 0,
            "red_cards": player_season.cards_red or 0,
            "fouls_committed": player_season.fouls_committed or 0,
            "fouls_drawn": player_season.fouls_drawn or 0,
            "penalties_scored": player_season.penalty_scored or 0,
            "penalties_missed": player_season.penalty_missed or 0,
            "penalties_won": player_season.penalty_won or 0,
            "goals_conceded": player_season.goals_conceded or 0,
            "saves": player_season.goals_saves or 0,
            "penalties_saved": player_season.penalty_saved or 0,
        }

    else:
        player_seasons = (
            db.query(PlayerSeason)
            .filter(PlayerSeason.player_id == player_id)
            .all()
        )

        if not player_seasons:
            return None

        stats = {
            "player_id": player_id,
            "season_id": None,
            "total_seasons": len(player_seasons),
            "total_matches_played": 0,
            "total_minutes_played": 0,
            "rating": 0,
            "total_goals": 0,
            "total_assists": 0,
            "total_shots": 0,
            "shots_on_target": 0,
            "total_tackles": 0,
            "tackles_blocks": 0,
            "tackles_interceptions": 0,
            "total_passes": 0,
            "key_passes": 0,
            "total_duels": 0,
            "duels_won": 0,
            "dribbles_success": 0,
            "dribbles_attempts": 0,
            "yellow_cards": 0,
            "red_cards": 0,
            "fouls_committed": 0,
            "fouls_drawn": 0,
            "penalties_scored": 0,
            "penalties_missed": 0,
            "penalties_won": 0,
            "goals_conceded": 0,
            "saves": 0,
            "penalties_saved": 0,
        }
        rating_sum = 0
        rating_count = 0

        for ps in player_seasons:
            stats["total_matches_played"] += ps.games_appearences or 0
            stats["total_minutes_played"] += ps.games_minutes or 0
            stats["total_goals"] += ps.goals_total or 0
            stats["total_assists"] += ps.goals_assists or 0
            stats["total_shots"] += ps.shots_total or 0
            stats["shots_on_target"] += ps.shots_on or 0
            stats["total_tackles"] += ps.tackles_total or 0
            stats["tackles_blocks"] += ps.tackles_blocks or 0
            stats["tackles_interceptions"] += ps.tackles_interceptions or 0
            stats["total_passes"] += ps.passes_total or 0
            stats["key_passes"] += ps.passes_key or 0
            stats["total_duels"] += ps.duels_total or 0
            stats["duels_won"] += ps.duels_won or 0
            stats["dribbles_success"] += ps.dribbles_success or 0
            stats["dribbles_attempts"] += ps.dribbles_attempts or 0
            stats["yellow_cards"] += ps.cards_yellow or 0
            stats["red_cards"] += ps.cards_red or 0
            stats["fouls_committed"] += ps.fouls_committed or 0
            stats["fouls_drawn"] += ps.fouls_drawn or 0
            stats["penalties_scored"] += ps.penalty_scored or 0
            stats["penalties_missed"] += ps.penalty_missed or 0
            stats["penalties_won"] += ps.penalty_won or 0
            stats["goals_conceded"] += ps.goals_conceded or 0
            stats["saves"] += ps.goals_saves or 0
            stats["penalties_saved"] += ps.penalty_saved or 0

            rating_sum += ps.games_rating or 0
            rating_count += 1

        avg_rating = round(rating_sum / rating_count, 1) if rating_count > 0 else None
        stats["rating"] = avg_rating

        return stats



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
            "name": r.name,
            "total_goals": r.total_goals,
            "total_game_appearances": r.total_game_appearances,
            "goals_per_match": round((r.total_goals or 0) / r.total_game_appearances, 3) if (r.total_game_appearances or 0) > 0 else 0
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
            "name": r.name,
            "total_shots": r.total_shots,
            "total_game_appearances": r.total_game_appearances,
            "shots_per_match": round((r.total_shots or 0) / r.total_game_appearances, 3) if (r.total_game_appearances or 0) > 0 else 0
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
            "name": r.name,
            "total_assists": r.total_assists,
            "total_game_appearances": r.total_game_appearances,
            "assists_per_match": round((r.total_assists or 0) / r.total_game_appearances, 3) if (r.total_game_appearances or 0) > 0 else 0
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
            "player_id": r.player_id,
            "name": r.name,
            "total_minutes": r.total_minutes,
            "total_game_appearances": r.total_game_appearances,
            "minutes_per_match": round(((r.total_minutes or 0) / r.total_game_appearances), 3) if (r.total_game_appearances or 0) > 0 else 0
        }
        for r in rows
    ]


@router.get("/penalty-success-rate")
def player_penalty_success_rate(
    player_id: int | None = Query(None, description="Filter to one player_id; if skipped return all players"),
    season_id: int | None = Query(None, description="Filter to one season_id; if skipped return all seasons"),
    db: Session = Depends(get_session)
    ):
    rows = player_queries(db, player_id, season_id, "penalty_success_rate")

    return [
        {
            "player_id": r.player_id,
            "name": r.name,
            "penalties_scored": r.penalties_scored,
            "penalties_missed": r.penalties_missed,
            "total_penalties": (r.penalties_scored) + (r.penalties_missed),
            "penalty_success_rate": round(((r.penalties_scored) / ((r.penalties_scored) + (r.penalties_missed))) * 100, 3
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
            "name": r.name,
            "total_shots": r.total_shots,
            "shots_on_target": r.shots_on_target,
            "accuracy_pct": round(((r.shots_on_target or 0) / (r.total_shots or 1)) * 100, 2
            ) if (r.total_shots and r.total_shots > 0) else 0
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
            detail=f"No data found for player_id: {player_id}" + (f" and season_id: {season_id}" if season_id else "")
        )

    return stats