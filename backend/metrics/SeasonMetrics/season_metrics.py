from fastapi import APIRouter, Depends, HTTPException, Query
from Database import get_session
from scripts.models_updated import Season, PlayerSeason, TeamSeason, Match, Team
from sqlalchemy.orm import Session
from sqlalchemy import func, case

router = APIRouter(prefix="/season-metrics", tags=["Season Metrics"])

# QUERY FUNCTIONS 

def get_season_aggregate_stats(db: Session, season_id: int):
    stats = db.query(
        func.sum(PlayerSeason.goals_total).label("total_goals"),
        func.sum(PlayerSeason.goals_assists).label("total_assists"),
        func.sum(PlayerSeason.cards_red).label("total_red_cards"),
        func.sum(PlayerSeason.cards_yellow).label("total_yellow_cards"),
        func.sum(PlayerSeason.shots_total).label("total_shots"),
        func.sum(PlayerSeason.shots_on).label("total_shots_on_target"),
        func.sum(PlayerSeason.tackles_total).label("total_tackles"),
        func.sum(PlayerSeason.duels_total).label("total_duels"),
        func.sum(PlayerSeason.duels_won).label("total_duels_won"),
        func.sum(PlayerSeason.passes_total).label("total_passes"),
        func.sum(PlayerSeason.passes_key).label("total_key_passes"),
        func.sum(PlayerSeason.dribbles_attempts).label("total_dribbles_attempts"),
        func.sum(PlayerSeason.dribbles_success).label("total_dribbles_success"),
        func.sum(PlayerSeason.fouls_committed).label("total_fouls_committed"),
        func.sum(PlayerSeason.fouls_drawn).label("total_fouls_drawn"),
        func.sum(PlayerSeason.penalty_scored).label("total_penalties_scored"),
        func.sum(PlayerSeason.penalty_missed).label("total_penalties_missed"),
        func.count(PlayerSeason.player_id).label("total_players"),
        func.sum(PlayerSeason.games_appearences).label("total_player_appearances"),
    ).filter(PlayerSeason.season_id == season_id).first()
    
    return stats


def get_team_ranking(db: Session, season_id: int):
    
    home_q = db.query(
        Match.home_team_id.label("team_id"),
        Match.teams_home_name.label("team_name"),
        Match.goals_home.label("gf"),
        Match.goals_away.label("ga"),
        case((Match.goals_home > Match.goals_away, 1), else_=0).label("is_win"),
        case((Match.goals_home == Match.goals_away, 1), else_=0).label("is_draw"),
        case((Match.goals_home < Match.goals_away, 1), else_=0).label("is_loss"),
    ).filter(Match.goals_home != None, Match.season_id == season_id)

    away_q = db.query(
        Match.away_team_id.label("team_id"),
        Match.teams_away_name.label("team_name"),
        Match.goals_away.label("gf"),
        Match.goals_home.label("ga"),
        case((Match.goals_away > Match.goals_home, 1), else_=0).label("is_win"),
        case((Match.goals_away == Match.goals_home, 1), else_=0).label("is_draw"),
        case((Match.goals_away < Match.goals_home, 1), else_=0).label("is_loss"),
    ).filter(Match.goals_away != None, Match.season_id == season_id)

    combined_subq = home_q.union_all(away_q).subquery()

    rows = db.query(
        combined_subq.c.team_id,
        combined_subq.c.team_name,
        func.count().label("matches"),
        func.sum(combined_subq.c.is_win).label("wins"),
        func.sum(combined_subq.c.is_draw).label("draws"),
        func.sum(combined_subq.c.is_loss).label("losses"),
        func.sum(combined_subq.c.gf).label("goals_for"),
        func.sum(combined_subq.c.ga).label("goals_against"),
    ).group_by(
        combined_subq.c.team_id, 
        combined_subq.c.team_name
    ).all()

    return rows


# ENDPOINTS 

@router.get("/stats")
def season_aggregate_stats(
    season_id: int,
    db: Session = Depends(get_session)
):
    stats = get_season_aggregate_stats(db, season_id)
    
    if not stats or stats.total_goals is None:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for season_id: {season_id}"
        )
    
    return {
        "season_id": season_id,
        "total_goals": stats.total_goals or 0,
        "total_assists": stats.total_assists or 0,
        "total_red_cards": stats.total_red_cards or 0,
        "total_yellow_cards": stats.total_yellow_cards or 0,
        "total_shots": stats.total_shots or 0,
        "total_shots_on_target": stats.total_shots_on_target or 0,
        "shot_accuracy_pct": round(
            ((stats.total_shots_on_target or 0) / (stats.total_shots or 1)) * 100, 2
        ) if stats.total_shots else 0,
        "total_tackles": stats.total_tackles or 0,
        "total_duels": stats.total_duels or 0,
        "total_duels_won": stats.total_duels_won or 0,
        "duel_win_rate_pct": round(
            ((stats.total_duels_won or 0) / (stats.total_duels or 1)) * 100, 2
        ) if stats.total_duels else 0,
        "total_passes": stats.total_passes or 0,
        "total_key_passes": stats.total_key_passes or 0,
        "total_dribbles_attempts": stats.total_dribbles_attempts or 0,
        "total_dribbles_success": stats.total_dribbles_success or 0,
        "dribble_success_rate_pct": round(
            ((stats.total_dribbles_success or 0) / (stats.total_dribbles_attempts or 1)) * 100, 2
        ) if stats.total_dribbles_attempts else 0,
        "total_fouls_committed": stats.total_fouls_committed or 0,
        "total_fouls_drawn": stats.total_fouls_drawn or 0,
        "total_penalties_scored": stats.total_penalties_scored or 0,
        "total_penalties_missed": stats.total_penalties_missed or 0,
        "total_players": stats.total_players or 0,
        "total_player_appearances": stats.total_player_appearances or 0,
    }


@router.get("/team-ranking")
def team_ranking(
    season_id: int,
    db: Session = Depends(get_session)
):
    rows = get_team_ranking(db, season_id)
    
    if not rows:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for season_id: {season_id}"
        )
    
    ranking_data = []
    for r in rows:
        points = (r.wins or 0) * 3 + (r.draws or 0)
        goal_diff = (r.goals_for or 0) - (r.goals_against or 0)
        
        ranking_data.append({
            "team_id": r.team_id,
            "team_name": r.team_name,
            "matches": r.matches,
            "wins": r.wins or 0,
            "draws": r.draws or 0,
            "losses": r.losses or 0,
            "goals_for": r.goals_for or 0,
            "goals_against": r.goals_against or 0,
            "goal_difference": goal_diff,
            "points": points,
            "points_per_match": round(points / (r.matches or 1), 3),
            "win_rate_pct": round(((r.wins or 0) / (r.matches or 1)) * 100, 2),
        })
    
    ranking_data.sort(key=lambda x: (x["points"], x["goal_difference"]), reverse=True)
    
    for rank, team in enumerate(ranking_data, 1):
        team["rank"] = rank
    
    return {
        "season_id": season_id,
        "ranking": ranking_data
    }