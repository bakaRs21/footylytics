import csv
import re
import asyncio
from pathlib import Path
from typing import Any, Optional
from sqlalchemy.orm import Session
from Database import Base, engine, get_session
from scripts.models_updated import (
    Season, Team, Nation, Referee,
    Player, TeamSeason, PlayerSeason, Match
)

def to_int(val: Any) -> Optional[int]:
    try:
        if val in (None, "", "None"):
            return None
        return int(float(str(val)))
    except ValueError:
        return None

def to_float(val: Any) -> Optional[float]:
    try:
        if val in (None, "", "None"):
            return None
        s = str(val).replace("%", "").strip()
        return float(s)
    except ValueError:
        return None

def to_bool(val: Any) -> Optional[bool]:
    if val in (None, "", "None"):
        return None
    str_val = str(val).strip().lower()
    if str_val in ("true", "t", "1", "yes", "y"):
        return True
    if str_val in ("false", "f", "0", "no", "n"):
        return False
    return None

def height_to_meters(raw: Any) -> Optional[float]:
    if raw in (None, "", "None"):
        return None
    str_raw = str(raw)
    if re.match(r"^\d\.\d+$", str_raw):
        try:
            return float(str_raw)
        except ValueError:
            return None
    digits = re.findall(r"\d+", str_raw)
    if digits:
        try:
            cm = int(digits[0])
            return round(cm / 100.0, 3)
        except ValueError:
            return None
    return None

TEAM_SEASON_FIELDS = {col.name for col in TeamSeason.__table__.columns if col.name not in ("team_id", "season_id")}
PLAYER_SEASON_FIELDS = {col.name for col in PlayerSeason.__table__.columns if col.name not in ("player_id", "season_id", "team_id")}
MATCH_FIELDS = {col.name for col in Match.__table__.columns}


def load_teams_and_seasons(teams_csv: Path, db: Session):
    with teams_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        existing_seasons = {sid for (sid,) in db.query(Season.season_id).all()}
        existing_teams = {tid for (tid,) in db.query(Team.team_id).all()}

        for row in reader:
            season_id = to_int(row.get("league_season"))
            if season_id and season_id not in existing_seasons:
                db.add(Season(season_id=season_id, season=str(season_id)))
                existing_seasons.add(season_id)

            team_id = to_int(row.get("team_id"))
            if team_id and team_id not in existing_teams:
                db.add(Team(
                    team_id=team_id,
                    name=row.get("team_name"),
                    logo=row.get("team_logo"),
                ))
                existing_teams.add(team_id)
        db.commit()

    with teams_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            season_id = to_int(row.get("league_season"))
            team_id = to_int(row.get("team_id"))
            if not season_id or not team_id:
                continue
            if db.get(TeamSeason, (team_id, season_id)):
                continue

            team_season_args = {"season_id": season_id, "team_id": team_id}
            for key, val in row.items():
                if key in TEAM_SEASON_FIELDS:
                    if "percentage" in key or "average" in key:
                        team_season_args[key] = to_float(val)
                    elif key.startswith(("fixtures_", "goals_", "clean_sheet", "failed_to_score", "penalty_", "cards_")):
                        team_season_args[key] = to_int(val)
                    else:
                        team_season_args[key] = val if val not in ("", "None") else None
            db.add(TeamSeason(**team_season_args))
        db.commit()

def load_players(players_csv: Path, db: Session):
    with players_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        nation_cache = {}
        existing_players = {pid for (pid,) in db.query(Player.player_id).all()}

        for row in reader:
            player_id = to_int(row.get("player_id"))
            if not player_id:
                continue

            nat_name = row.get("nationality") or "Unknown"
            if nat_name not in nation_cache:
                existing = db.query(Nation).filter_by(nation_name=nat_name).first()
                if existing:
                    nation_cache[nat_name] = existing.nation_id
                else:
                    nat_obj = Nation(nation_name=nat_name)
                    db.add(nat_obj)
                    db.flush()
                    nation_cache[nat_name] = nat_obj.nation_id

            if player_id not in existing_players:
                db.add(Player(
                    player_id=player_id,
                    name=row.get("player_name"),
                    age=to_int(row.get("age")),
                    nation_id=nation_cache[nat_name],
                    height_in_m=height_to_meters(row.get("height")),
                    weight=to_int(row.get("weight")),
                ))
                existing_players.add(player_id)
        db.commit()

    with players_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            player_id = to_int(row.get("player_id"))
            season_id = to_int(row.get("season"))
            team_id = to_int(row.get("team_id"))
            if not (player_id and season_id and team_id):
                continue
            if db.get(PlayerSeason, (player_id, season_id, team_id)):
                continue

            player_season_args = {"player_id": player_id, "season_id": season_id, "team_id": team_id}
            for key, val in row.items():
                if key in PLAYER_SEASON_FIELDS:
                    if key == "games_rating":
                        player_season_args[key] = to_float(val)
                    elif key.startswith(("games_", "substitutes_", "shots_", "goals_", "passes_", "tackles_", "duels_", "dribbles_", "fouls_", "cards_", "penalty_")):
                        player_season_args[key] = to_int(val)
                    else:
                        player_season_args[key] = val if val not in ("", "None") else None
            db.add(PlayerSeason(**player_season_args))
        db.commit()

def load_matches(matches_csv: Path, db: Session):
    with matches_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        ref_cache = {}
        existing_matches = {fid for (fid,) in db.query(Match.fixture_id).all()}
        existing_seasons = {sid for (sid,) in db.query(Season.season_id).all()}
        existing_teams = {tid for (tid,) in db.query(Team.team_id).all()}

        for row in reader:
            fixture_id = to_int(row.get("fixture_id"))
            if not fixture_id:
                continue
            if fixture_id in existing_matches:
                continue

            season_id = to_int(row.get("league_season")) or to_int(row.get("season"))
            if season_id and season_id not in existing_seasons:
                db.add(Season(season_id=season_id, season=str(season_id)))
                db.flush()
                existing_seasons.add(season_id)

            home_id = to_int(row.get("teams_home_id")) or to_int(row.get("home_team_id"))
            away_id = to_int(row.get("teams_away_id")) or to_int(row.get("away_team_id"))
            for tid, tname, tlogo in [
                (home_id, row.get("teams_home_name"), row.get("teams_home_logo")),
                (away_id, row.get("teams_away_name"), row.get("teams_away_logo")),
            ]:
                if tid and tid not in existing_teams:
                    db.add(Team(team_id=tid, name=tname, logo=tlogo))
                    existing_teams.add(tid)
            db.flush()

            ref_name = row.get("fixture_referee")
            referee_id = None
            if ref_name:
                if ref_name in ref_cache:
                    referee_id = ref_cache[ref_name]
                else:
                    existing = db.query(Referee).filter_by(name=ref_name).first()
                    if existing:
                        referee_id = existing.referee_id
                    else:
                        ref_obj = Referee(name=ref_name)
                        db.add(ref_obj)
                        db.flush()
                        referee_id = ref_obj.referee_id
                    ref_cache[ref_name] = referee_id

            match_args = {"fixture_id": fixture_id}
            for key, val in row.items():
                if key not in MATCH_FIELDS or key == "fixture_id":
                    continue
                if key in ("fixture_timestamp", "fixture_periods_first", "fixture_periods_second",
                         "fixture_venue_id", "fixture_status_elapsed", "fixture_status_extra",
                         "league_id", "score_halftime_home", "score_halftime_away",
                         "score_fulltime_home", "score_fulltime_away",
                         "score_extratime_home", "score_extratime_away",
                         "score_penalty_home", "score_penalty_away",
                         "goals_home", "goals_away"):
                    match_args[key] = to_int(val)
                elif key in ("league_standings", "teams_home_winner", "teams_away_winner"):
                    match_args[key] = to_bool(val)
                else:
                    match_args[key] = val if val not in ("", "None") else None

            if referee_id is not None:
                match_args["referee_id"] = referee_id
            if season_id:
                match_args["season_id"] = season_id
            if home_id:
                match_args["home_team_id"] = home_id
            if away_id:
                match_args["away_team_id"] = away_id

            db.add(Match(**match_args))
            existing_matches.add(fixture_id)
        db.commit()

def run_loader_once(db: Session):
    base = Path(__file__).resolve().parent.parent
    teams_csv = base / "datasets" / "Teams_2010-2024.csv"
    players_csv = base / "datasets" / "Players_2010-2024.csv"
    matches_csv = base / "datasets" / "All_Matches_2010-2024_cleaned.csv"

    Base.metadata.create_all(bind=engine)

    load_teams_and_seasons(teams_csv, db)
    load_players(players_csv, db)
    load_matches(matches_csv, db)

async def run_loader_periodically(interval_seconds: int = 6 * 60 * 60):
    while True:
        await asyncio.sleep(interval_seconds)
        db_gen = get_session()
        db = next(db_gen)
        try:
            await asyncio.to_thread(run_loader_once, db)
        finally:
            try:
                next(db_gen)
            except StopIteration:
                pass

if __name__ == "__main__":
    run_loader_once()