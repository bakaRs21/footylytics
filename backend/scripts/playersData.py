from Database import get_session
from scripts.models_updated import Player, PlayerSeason, Season
from typing import List
from sqlalchemy.orm import load_only




    #get all players
async def players(limit: int = 5000) -> List[Player]:
    session = get_session()
    try:
        return session.query(Player).options(load_only(Player.player_id, Player.name)).limit(limit).all()
    finally:
        session.close()

    # Get seasons for a specific player
def player_seasons(player_id: int):
    session = get_session()
    try:
        player = session.query(Season).join(PlayerSeason).options(load_only(Season.season_id, Season.season)).filter(PlayerSeason.player_id == player_id).all()
        if not player:
            raise ValueError(f"Player with id {player_id} not found")
        return player
    finally:
        session.close()

    # get all players from specific season
def players_from_season(season: str):
    session = get_session()
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
def player_info(player_id: int):
    session = get_session()
    try:
        return session.query(Player).filter(Player.player_id == player_id).first()
    finally:
        session.close()

    # Get player stats for a specific player and season
async def player_stats_from_season(player_id: int, season_id: int):
    session = get_session()
    try:
        stats = (session.query(PlayerSeason)
                .join(Player, Player.player_id == PlayerSeason.player_id)
                .filter(Player.player_id == player_id, PlayerSeason.season_id == season_id)
                .all()
        )
        if not stats:
            raise ValueError(f"Stats for player id {player_id} in season id {season_id} not found")
        
        return stats
    finally:
        session.close()