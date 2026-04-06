from sqlalchemy import Integer, func
from scripts.models_updated import Player, PlayerSeason, Season, Nation, Team
from typing import List
from sqlalchemy.orm import load_only, Session, joinedload
from sqlalchemy.inspection import inspect


    #get all players
async def players(limita, session: Session) -> List[Player]:
    limit = limita
    if not limit:
        limit = 4000
    try:
        return session.query(Player).options(load_only(Player.player_id, Player.name)).limit(limit).all()
    finally:
        session.close()

    # Get seasons for a specific player
def player_seasons(player_id: int, session: Session):
    try:
        seasons = (session.query(Season.season)
                  .join(PlayerSeason, PlayerSeason.season_id == Season.season_id)
                  .filter(PlayerSeason.player_id == player_id)
                  .all())
        if not seasons:
            raise ValueError(f"Player with id {player_id} not found")
        flat_seasons = [s[0] for s in seasons]
        return flat_seasons
    finally:
        session.close()

    # get all players from specific season
def players_from_season(season: str, session: Session):
    try:
        players = (
            session.query(Player)
            .join(PlayerSeason, PlayerSeason.player_id == Player.player_id)
            .join(Season, PlayerSeason.season_id == Season.season_id)
            .options(load_only(Player.player_id, Player.name))
            .filter(Season.season == season).all()
            )
        return players
    finally:
        session.close()

    # Get general info about a specific player
def player_info(player_id: int, session: Session):
    try:
        return (session.query(Player)
                .options(joinedload(Player.nation))
                .filter(Player.player_id == player_id)
                .first())
    finally:
        session.close()

    # Get player stats for a specific player and season
async def player_stats_from_season(player_id: int, season_id: int, session: Session):
    try:
        if season_id is None:
            stats = player_stats_builder(player_id, session)
            player_stats = stats._asdict()
        else:
            player_stats = (session.query(PlayerSeason)
                    .join(Player, Player.player_id == PlayerSeason.player_id)
                    .filter(Player.player_id == player_id, PlayerSeason.season_id == season_id)
                    .all()
            )
        if not player_stats:
            raise ValueError(f"Stats for player id {player_id} in season id {season_id} not found")
        
        return player_stats
    finally:
        session.close()

def player_with_seasons_teams(session: Session):
    try:
        players = (session.query(Player).join(PlayerSeason).join(Season).join(Team).options(
            joinedload(Player.player_seasons)
            .joinedload(PlayerSeason.team),
            joinedload(Player.player_seasons)
            .joinedload(PlayerSeason.season)
        ).all())
        if not players:
            raise ValueError("No players with seasons and teams found")
        
        return [
            {
                'player_id': player.player_id,
                'name': player.name,
                'seasons': [
                    {
                        'season_id': season.season.season_id,
                        'season': season.season.season,
                    }
                    for season in player.player_seasons
                ],
                'teams': [
                    {
                        'team_id': team.team.team_id,
                        'name': team.team.name,
                    }
                    for team in player.player_seasons
                ]
            }
            for player in players
        ]
    finally:
        session.close()