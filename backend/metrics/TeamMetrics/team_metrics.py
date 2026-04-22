from fastapi import APIRouter, Depends, HTTPException
from Database import get_session
from scripts.models_updated import Team, TeamSeason, Match
from sqlalchemy import func, case
from sqlalchemy.orm import Session

router = APIRouter(prefix="/team-metrics", tags=["Team Metrics"])

# QUERIES _____________________________________________________________________________________
def get_match_aggregates(db: Session, team_id: int | None, season_id: int | None):
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


def get_goal_difference(db: Session, team_id: int | None, season_id: int | None):

    home_q = db.query(
        Match.home_team_id.label("team_id"),
        Match.teams_home_name.label("team_name"),
        Match.goals_home.label("gf"),
        Match.goals_away.label("ga"),
    ).filter(Match.goals_home != None)

    away_q = db.query(
        Match.away_team_id.label("team_id"),
        Match.teams_away_name.label("team_name"),
        Match.goals_away.label("gf"),
        Match.goals_home.label("ga"),
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
        func.sum(combined_subq.c.gf).label("gf"),
        func.sum(combined_subq.c.ga).label("ga"),
    ).group_by(combined_subq.c.team_id, combined_subq.c.team_name).all()

    return rows

def get_basic_team_stats(db: Session, team_id: int, season_id: int | None):
    if season_id:
        team_season = (
            db.query(TeamSeason)
            .filter(TeamSeason.team_id == team_id, TeamSeason.season_id == season_id)
            .first()
        )
        
        if not team_season:
            return None
        
        return {
            "team_id": team_season.team_id,
            "season_id": team_season.season_id,
            "form": team_season.form,
            "lineups": team_season.lineups,
            "total_matches_played": (
                (team_season.fixtures_played_home or 0) + 
                (team_season.fixtures_played_away or 0)
            ),
            "total_wins": (
                (team_season.fixtures_wins_home or 0) + 
                (team_season.fixtures_wins_away or 0)
            ),
            "total_draws": (
                (team_season.fixtures_draws_home or 0) + 
                (team_season.fixtures_draws_away or 0)
            ),
            "total_losses": (
                (team_season.fixtures_loses_home or 0) + 
                (team_season.fixtures_loses_away or 0)
            ),
            "total_goals_scored": (
                (team_season.goals_for_total_home or 0) + 
                (team_season.goals_for_total_away or 0)
            ),
            "total_goals_conceded": (
                (team_season.goals_against_total_home or 0) + 
                (team_season.goals_against_total_away or 0)
            ),
            "total_clean_sheets": (
                (team_season.clean_sheet_home or 0) + 
                (team_season.clean_sheet_away or 0)
            ),
            "total_failed_to_score": (
                (team_season.failed_to_score_home or 0) + 
                (team_season.failed_to_score_away or 0)
            ),
            "total_penalties_scored": team_season.penalty_scored_total,
            "total_penalties_missed": team_season.penalty_missed_total,
            "biggest_win_streak": team_season.biggest_streak_wins,
            "biggest_draw_streak": team_season.biggest_streak_draws,
            "biggest_lose_streak": team_season.biggest_streak_loses,
        }
    
    else:
        team_seasons = (
            db.query(TeamSeason)
            .filter(TeamSeason.team_id == team_id)
            .all()
        )
        
        if not team_seasons:
            return None
        
        stats = {
            "team_id": team_id,
            "season_id": None,
            "total_seasons": len(team_seasons),
            "form": None,
            "lineups": None,
            "total_matches_played": 0,
            "total_wins": 0,
            "total_draws": 0,
            "total_losses": 0,
            "total_goals_scored": 0,
            "total_goals_conceded": 0,
            "total_clean_sheets": 0,
            "total_failed_to_score": 0,
            "total_penalties_scored": 0,
            "total_penalties_missed": 0,
            "biggest_win_streak": 0,
            "biggest_draw_streak": 0,
            "biggest_lose_streak": 0,
        }
        
        for ts in team_seasons:
            stats["total_matches_played"] += (
                (ts.fixtures_played_home or 0) + 
                (ts.fixtures_played_away or 0)
            )
            stats["total_wins"] += (
                (ts.fixtures_wins_home or 0) + 
                (ts.fixtures_wins_away or 0)
            )
            stats["total_draws"] += (
                (ts.fixtures_draws_home or 0) + 
                (ts.fixtures_draws_away or 0)
            )
            stats["total_losses"] += (
                (ts.fixtures_loses_home or 0) + 
                (ts.fixtures_loses_away or 0)
            )
            stats["total_goals_scored"] += (
                (ts.goals_for_total_home or 0) + 
                (ts.goals_for_total_away or 0)
            )
            stats["total_goals_conceded"] += (
                (ts.goals_against_total_home or 0) + 
                (ts.goals_against_total_away or 0)
            )
            stats["total_clean_sheets"] += (
                (ts.clean_sheet_home or 0) + 
                (ts.clean_sheet_away or 0)
            )
            stats["total_failed_to_score"] += (
                (ts.failed_to_score_home or 0) + 
                (ts.failed_to_score_away or 0)
            )
            stats["total_penalties_scored"] += (ts.penalty_scored_total or 0)
            stats["total_penalties_missed"] += (ts.penalty_missed_total or 0)
            
            stats["biggest_win_streak"] = max(
                stats["biggest_win_streak"], 
                int(ts.biggest_streak_wins) if ts.biggest_streak_wins is not None else 0
            )
            stats["biggest_draw_streak"] = max(
                stats["biggest_draw_streak"], 
                int(ts.biggest_streak_draws) if ts.biggest_streak_draws is not None else 0
            )
            stats["biggest_lose_streak"] = max(
                stats["biggest_lose_streak"], 
                int(ts.biggest_streak_loses) if ts.biggest_streak_loses is not None else 0
            )
        
        return stats

def get_team_season_data(db: Session, team_id: int | None, season_id: int | None):
    q = db.query(TeamSeason)
    
    if team_id is not None:
        q = q.filter(TeamSeason.team_id == team_id)
    
    if season_id is not None:
        q = q.filter(TeamSeason.season_id == season_id)
    
    return q.all()


# METRIC ENDPOINTS _____________________________________________________________________________________
@router.get("/goals-scored-per-match")
def goals_scored_per_match(
    team_id: int | None = None,
    season_id: int | None = None,
    db: Session = Depends(get_session)
):
    rows = get_match_aggregates(db, team_id, season_id)
    result = []
    for r in rows:
        result.append({
            "team_id": r.team_id,
            "team_name": r.team_name,
            "goals_scored_per_match": round((r.gf or 0) / (r.matches or 1), 3),
            "team_goals": r.gf,
            "matches": r.matches
        })
    
    return result


@router.get("/goals-conceded-per-match")
def goals_conceded_per_match(
    team_id: int | None = None,
    season_id: int | None = None,
    db: Session = Depends(get_session),
):
    rows = get_match_aggregates(db, team_id, season_id)
    result = []
    for r in rows:
        result.append({
            "team_id": r.team_id,
            "team_name": r.team_name,
            "goals_conceded_per_match": round((r.ga or 0) / (r.matches or 1), 3),
            "team_goals_conceded": r.ga,
            "matches": r.matches,
        })
    
    return result


@router.get("/goal-difference-per-match")
def goal_difference_per_match(
    team_id: int | None = None,
    season_id: int | None = None,
    db: Session = Depends(get_session),
):
    rows = get_match_aggregates(db, team_id, season_id)
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
    team_id: int | None = None,
    season_id: int | None = None,
    db: Session = Depends(get_session),
):
    rows = get_goal_difference(db, team_id, season_id)
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

@router.get("/points-per-match")
def points_per_match(
    team_id: int | None = None,
    season_id: int | None = None,
    db: Session = Depends(get_session),
):
    rows = get_match_aggregates(db, team_id, season_id)
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
    team_id: int | None = None,
    season_id: int | None = None,
    db: Session = Depends(get_session),
):
    rows = get_match_aggregates(db, team_id, season_id)
    
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


@router.get("/points-per-goal-scored")
def points_per_goal_scored(
    team_id: int | None = None,
    season_id: int | None = None,
    db: Session = Depends(get_session),
):
    rows = get_match_aggregates(db, team_id, season_id)
    
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
    team_id: int | None = None,
    season_id: int | None = None,
    db: Session = Depends(get_session),
):
    team_seasons = get_team_season_data(db, team_id, season_id)
    results = []
    for ts in team_seasons:
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
def goals_scored_percentage_by_minutes(
    team_id: int | None = None,
    season_id: int | None = None,
    db: Session = Depends(get_session)
):
    team_seasons = get_team_season_data(db, team_id, season_id)
    result = []
    for ts in team_seasons:
        result.append({
            "team_id": ts.team_id,
            "season_id": ts.season_id,
            "minutes_0_15": {
                "total": ts.goals_for_minute_0_15_total,
                "percentage": ts.goals_for_minute_0_15_percentage
            },
            "minutes_16_30": {
                "total": ts.goals_for_minute_16_30_total,
                "percentage": ts.goals_for_minute_16_30_percentage
            },
            "minutes_31_45": {
                "total": ts.goals_for_minute_31_45_total,
                "percentage": ts.goals_for_minute_31_45_percentage
            },
            "minutes_46_60": {
                "total": ts.goals_for_minute_46_60_total,
                "percentage": ts.goals_for_minute_46_60_percentage
            },
            "minutes_61_75": {
                "total": ts.goals_for_minute_61_75_total,
                "percentage": ts.goals_for_minute_61_75_percentage
            },
            "minutes_76_90": {
                "total": ts.goals_for_minute_76_90_total,
                "percentage": ts.goals_for_minute_76_90_percentage
            },
            "minutes_91_105": {
                "total": ts.goals_for_minute_91_105_total,
                "percentage": ts.goals_for_minute_91_105_percentage
            },
            "minutes_106_120": {
                "total": ts.goals_for_minute_106_120_total,
                "percentage": ts.goals_for_minute_106_120_percentage
            },
        })
    
    return result


@router.get("/goals-conceded-percentage-by-minutes")
def goals_conceded_percentage_by_minutes(
    team_id: int | None = None,
    season_id: int | None = None,
    db: Session = Depends(get_session)
):
    team_seasons = get_team_season_data(db, team_id, season_id)
    result = []
    for ts in team_seasons:
        result.append({
            "team_id": ts.team_id,
            "season_id": ts.season_id,
            "minutes_0_15": {
                "total": ts.goals_against_minute_0_15_total,
                "percentage": ts.goals_against_minute_0_15_percentage
            },
            "minutes_16_30": {
                "total": ts.goals_against_minute_16_30_total,
                "percentage": ts.goals_against_minute_16_30_percentage
            },
            "minutes_31_45": {
                "total": ts.goals_against_minute_31_45_total,
                "percentage": ts.goals_against_minute_31_45_percentage
            },
            "minutes_46_60": {
                "total": ts.goals_against_minute_46_60_total,
                "percentage": ts.goals_against_minute_46_60_percentage
            },
            "minutes_61_75": {
                "total": ts.goals_against_minute_61_75_total,
                "percentage": ts.goals_against_minute_61_75_percentage
            },
            "minutes_76_90": {
                "total": ts.goals_against_minute_76_90_total,
                "percentage": ts.goals_against_minute_76_90_percentage
            },
            "minutes_91_105": {
                "total": ts.goals_against_minute_91_105_total,
                "percentage": ts.goals_against_minute_91_105_percentage
            },
            "minutes_106_120": {
                "total": ts.goals_against_minute_106_120_total,
                "percentage": ts.goals_against_minute_106_120_percentage
            }
        })
    
    return result

@router.get("/basic-stats")
def basic_team_stats(
    team_id: int,
    season_id: int | None = None,
    db: Session = Depends(get_session),
):
    stats = get_basic_team_stats(db, team_id, season_id)
    if not stats:
        raise HTTPException(
            status_code=404, 
            detail=f"No data found for team_id={team_id}" + (f" and season_id={season_id}" if season_id else "")
        )
    
    return stats