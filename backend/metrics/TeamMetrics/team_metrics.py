from fastapi import APIRouter, Query, Depends, HTTPException
from Database import get_session
from scripts.models_updated import Team, TeamSeason, Match
from sqlalchemy import func, case
from sqlalchemy.orm import Session

router = APIRouter(prefix="/team-metrics", tags=["Team Metrics"])

def aggregate_matches(db: Session, team_id: int | None, season_id: int | None):
    home_q = db.query(
        Match.home_team_id.label("team_id"),
        Match.teams_home_name.label("team_name"),
        Match.goals_home.label("gf"),
        Match.goals_away.label("ga"),
        case((Match.goals_home > Match.goals_away, 1), else_=0).label("is_win"),
        case((Match.goals_home == Match.goals_away, 1), else_=0).label("is_draw"),
    ).filter(Match.goals_home != None)

    away_q = db.query(
        Match.away_team_id.label("team_id"),
        Match.teams_away_name.label("team_name"),
        Match.goals_away.label("gf"),
        Match.goals_home.label("ga"),
        case((Match.goals_away > Match.goals_home, 1), else_=0).label("is_win"),
        case((Match.goals_away == Match.goals_home, 1), else_=0).label("is_draw"),
    ).filter(Match.goals_away != None)

    if team_id is not None:
        home_q = home_q.filter(Match.home_team_id == team_id)
        away_q = away_q.filter(Match.away_team_id == team_id)

    if season_id is not None:
        home_q = home_q.filter(Match.season_id == season_id)
        away_q = away_q.filter(Match.season_id == season_id)

    combined_subq = home_q.union_all(away_q).subquery()

    rows = db.query(
        combined_subq.c.team_id,
        combined_subq.c.team_name,
        func.count().label("matches"),
        func.sum(combined_subq.c.gf).label("gf"),
        func.sum(combined_subq.c.ga).label("ga"),
        func.sum(combined_subq.c.is_win).label("wins"),
        func.sum(combined_subq.c.is_draw).label("draws"),
    ).group_by(combined_subq.c.team_id, combined_subq.c.team_name).all()

    return rows

def aggregate_goals_by_15_minutes(db: Session, team_id: Optional[int], season_id: Optional[int]):
    goals_scored = db.query(
        
    )


@router.get("/goals-conceded-per-match")
def goals_conceded_per_match(
    team_id: int | None = Query(None),
    season_id: int | None = Query(None),
    db: Session = Depends(get_session),
):
    rows = aggregate_matches(db, team_id, season_id)
    result = []
    for r in rows:
        result.append({
            "team_id": r.team_id,
            "team_name": r.team_name,
            "avg_goals_conceded_per_match": round((r.ga or 0) / (r.matches or 1), 3),
            "matches": r.matches,
        })
    return result

@router.get("/goals-scored-per-match")
def goals__scored_per_match(
    team_id: Optional[int] = Query(None),
    season_id: Optional[int] = Query(None),
    db: Session = Depends(get_session)
):
    rows = aggregate_matches(db, team_id, season_id)
    result = []
    for r in rows:
        result.append({
            "team_id": r.team_id,
            "team_name":r.team_name,
            "avg_goals_scored_per_match": round((r.gf or 0) / (r.matches or 1), 3),
            "team_goals": r.gf,
            "matches": r.matches
        })
        
    return result

@router.get("/points-per-match")
def points_per_match(
    team_id: int | None = Query(None),
    season_id: int | None = Query(None),
    db: Session = Depends(get_session),
):
    rows = aggregate_matches(db, team_id, season_id)
    result = []
    for r in rows:
        points = (r.wins or 0) * 3 + (r.draws or 0) * 1
        ppm = points / (r.matches or 1)
        result.append({
            "team_id": r.team_id,
            "team_name": r.team_name,
            "points": points,
            "matches": r.matches,
            "points_per_match": round(ppm, 3),
        })
    return result

@router.get("/win-rate")
def win_rate(
    team_id: int | None = Query(None),
    season_id: int | None = Query(None),
    db: Session = Depends(get_session),
):
    rows = aggregate_matches(db, team_id, season_id)
    return [
        {
            "team_id": r.team_id,
            "team_name": r.team_name,
            "wins": r.wins,
            "matches": r.matches,
            "win_rate_pct": round(((r.wins or 0) / (r.matches or 1)) * 100, 2),
        }
        for r in rows
    ]

@router.get("/goal-difference-per-match")
def goal_difference_per_match(
    team_id: int | None = Query(None),
    season_id: int | None = Query(None),
    db: Session = Depends(get_session),
):
    rows = aggregate_matches(db, team_id, season_id)
    return [
        {
            "team_id": r.team_id,
            "team_name": r.team_name,
            "goal_diff": (r.gf or 0) - (r.ga or 0),
            "matches": r.matches,
            "goal_diff_per_match": round(((r.gf or 0) - (r.ga or 0)) / (r.matches or 1), 3),
        }
        for r in rows
    ]

@router.get("/attack-defense-balance")
def attack_defense_balance(
    team_id: int | None = Query(None),
    season_id: int | None = Query(None),
    db: Session = Depends(get_session),
):
    rows = aggregate_matches(db, team_id, season_id)
    return [
        {
            "team_id": r.team_id,
            "team_name": r.team_name,
            "attack_defense_balance": (r.gf or 0) - (r.ga or 0),
            "goals_for": r.gf,
            "goals_against": r.ga,
        }
        for r in rows
    ]

@router.get("/points-per-goal-scored")
def points_per_goal_scored(
    team_id: int | None = Query(None),
    season_id: int | None = Query(None),
    db: Session = Depends(get_session),
):
    rows = aggregate_matches(db, team_id, season_id)
    out = []
    for r in rows:
        points = (r.wins or 0) * 3 + (r.draws or 0)
        if r.gf and r.gf > 0:
            ppg = points / r.gf
        else:
            ppg = None
        out.append({
            "team_id": r.team_id,
            "team_name": r.team_name,
            "points": points,
            "goals_for": r.gf,
            "points_per_goal_scored": round(ppg, 3) if ppg is not None else None,
        })
    return out

@router.get("/season-consistency-index")
def season_consistency_index(
    team_id: int | None = Query(None),
    season_id: int | None = Query(None),
    db: Session = Depends(get_session),
):
    """(wins + losses) / matches_played, from TeamSeason aggregates."""
    q = db.query(TeamSeason)
    if team_id is not None:
        q = q.filter(TeamSeason.team_id == team_id)
    if season_id is not None:
        q = q.filter(TeamSeason.season_id == season_id)

    results = []
    for ts in q.all():
        wins = (ts.fixtures_wins_home or 0) + (ts.fixtures_wins_away or 0)
        losses = (ts.fixtures_loses_home or 0) + (ts.fixtures_loses_away or 0)
        matches = (ts.fixtures_played_home or 0) + (ts.fixtures_played_away or 0)
        idx = ((wins + losses) / matches) if matches else None
        results.append({
            "team_id": ts.team_id,
            "season_id": ts.season_id,
            "wins": wins,
            "losses": losses,
            "matches": matches,
            "season_consistency_index": round(idx, 3) if idx is not None else None,
        })
    return results

@router.get("/goals-scored-percentage-by-minutes")
def  scored_gaols_percentage_by_minutes(
    team_id: Optional[int] = Query(None),
    season_id: Optional[int] = Query(None),
    db: Session = Depends(get_session)
):
    rows = aggregate_matches(team_id, season_id, db)
    result = []
    for r in rows:
        result.append(

        )