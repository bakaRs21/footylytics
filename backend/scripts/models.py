from sqlalchemy import INT, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from Database import Base


# MAIN TABLE/OBJECT
class Seasons(Base):
    __tablename__ = 'seasons'
    season_id = Column(Integer, primary_key=True, index=True)
    season = Column(String)

#----------------------------------------------
# INFERIOR TABLES/OBJECTS
#----------------------------------------------

# TEAM TABLE/OBJECT
class Teams(Base):
    __tablename__ = 'teams'
    team_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

# PLAYER TABLE/OBJECT
class Players(Base):
    __tablename__ = 'players'
    player_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date_of_birth = Column(DateTime)
    foot = Column(String, nullable=True)
    height_in_meters = Column(Float, nullable=True)
    nationality = Column(String)

# REFEREE TABLE/OBJECT
class Referees(Base):
    __tablename__ = 'referees'
    referee_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

#-----------------------------------------------
# ASSOCIATIVE TABLES/OBJECTS
#-----------------------------------------------

# TEAM HAS SEASON TABLE/OBJECT
class TeamHasSeason(Base):
    __tablename__ = 'team_has_season'
    team_id = Column(Integer, ForeignKey("teams.team_id"), primary_key=True)
    season_id = Column(Integer, ForeignKey("seasons.season_id"), primary_key=True)
    standing_position = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    draws = Column(Integer)
    total_yel_card = Column(Integer, nullable=True)
    total_red_card = Column(Integer, nullable=True)
    total_shots_att = Column(Integer, nullable=True)
    on_target_shots = Column(Integer, nullable=True)
    hit_woodwork = Column(Integer, nullable=True)
    att_header_goal = Column(Integer, nullable=True)
    att_pen_goal = Column(Integer, nullable=True)
    att_freekick_goal = Column(Integer, nullable=True)
    att_in_box_goal = Column(Integer, nullable=True)
    att_out_box_goal  = Column(Integer, nullable=True)
    goal_fastbreak  = Column(Integer, nullable=True)
    total_offsides = Column(Integer, nullable=True)
    clean_sheet = Column(Integer, nullable=True)
    goals_conceded = Column(Integer, nullable=True)
    saves = Column(Integer, nullable=True)
    outfielder_block = Column(Integer, nullable=True)
    intercpetion = Column(Integer, nullable=True)
    total_tackles = Column(Integer, nullable=True)
    last_man_tackle = Column(Integer, nullable=True)
    total_clearance = Column(Integer, nullable=True)
    head_clearance = Column(Integer, nullable=True)
    own_goals = Column(Integer, nullable=True)
    penalty_conceded = Column(Integer, nullable=True)
    pen_goals_conceded = Column(Integer, nullable=True)
    total_passes = Column(Integer, nullable=True)
    total_through_ball = Column(Integer, nullable=True)
    total_long_ball = Column(Integer, nullable=True)
    backward_pass = Column(Integer, nullable=True)
    total_cross = Column(Integer, nullable=True)
    corners_taken = Column(Integer, nullable=True)
    touches = Column(Integer, nullable=True)
    big_chance_missed = Column(Integer, nullable=True)
    clearance_off_line = Column(Integer, nullable=True)
    disposessed = Column(Integer, nullable=True)
    penalty_saved = Column(Integer, nullable=True)
    total_high_claim = Column(Integer, nullable=True)
    punches = Column(Integer, nullable=True)

    teams = relationship("Teams")
    seasons = relationship("Seasons")

# PLAYER HAS SEASONS + TEAMS TABLE/OBJECT
class PlayerHasSeasons(Base):
    __tablename__ = 'player_has_seasons'
    player_id = Column(Integer, ForeignKey("players.player_id"), primary_key=True)
    season_id = Column(Integer, ForeignKey("seasons.season_id"), primary_key=True)
    team_id = Column(Integer, ForeignKey("teams.team_id"))
    market_value = Column(String, nullable=True)
    position = Column(String, nullable=True)
    signed_from = Column(String, nullable=True)
    jersey_number = Column(Integer, nullable=True)
    appearances = Column(Integer, nullable=True)
    wins = Column(Integer, nullable=True)
    losses = Column(Integer, nullable=True)
    draws = Column(Integer, nullable=True)
    goals_per_match = Column(Float, nullable=True)
    header_goals = Column(Integer, nullable=True)
    right_foot_goals = Column(Integer, nullable=True)
    left_foot_goals = Column(Integer, nullable=True)
    pen_goals = Column(Integer, nullable=True)
    freekick_goals = Column(Integer, nullable=True)
    shots_total = Column(Integer, nullable=True)
    shots_on_target = Column(Integer, nullable=True)
    hit_woodwork = Column(Integer, nullable=True)
    big_chances_missed = Column(Integer, nullable=True)
    clean_sheets = Column(Integer, nullable=True)
    goals_conceded = Column(Integer, nullable=True)
    tackles = Column(Integer, nullable=True)
    last_man_tackles = Column(Integer, nullable=True)
    blocked_shots = Column(Integer, nullable=True)
    clearances = Column(Integer, nullable=True)
    header_clearances = Column(Integer, nullable=True)
    interceptions = Column(Integer, nullable=True)
    recoveries = Column(Integer, nullable=True)
    duels_won = Column(Integer, nullable=True)
    duels_lost = Column(Integer, nullable=True)
    aerial_battles_won = Column(Integer, nullable=True)
    aerial_battles_lost = Column(Integer, nullable=True)
    own_goals = Column(Integer, nullable=True)
    errors_leading_to_goal = Column(Integer, nullable=True)
    assists = Column(Integer, nullable=True)
    passes_total = Column(Integer, nullable=True)
    big_chances_created = Column(Integer, nullable=True)
    crosses_total = Column(Integer, nullable=True)
    through_balls = Column(Integer, nullable=True)
    accurate_long_balls = Column(Integer, nullable=True)
    saves = Column(Integer, nullable=True)
    penalties_saved = Column(Integer, nullable=True)
    punches = Column(Integer, nullable=True)
    high_claims = Column(Integer, nullable=True)
    catches = Column(Integer, nullable=True)
    throw_outs = Column(Integer, nullable=True)
    goal_kicks = Column(Integer, nullable=True)
    yellow_cards = Column(Integer, nullable=True)
    red_cards = Column(Integer, nullable=True)
    fouls_committed = Column(Integer, nullable=True)
    offsides = Column(Integer, nullable=True)

    players = relationship("Players")
    seasons = relationship("Seasons")
    teams = relationship("Teams")

# ALL MATCHES TABLE/OBJECT

class AllMatches(Base):
    __tablename__ = 'all_matches'
    match_id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, ForeignKey("seasons.season_id"))
    referee_id = Column(Integer, ForeignKey("referees.referee_id"))
    date = Column(DateTime)
    home_team_id = Column(Integer, ForeignKey("teams.team_id"))
    away_team_id = Column(Integer, ForeignKey("teams.team_id"))
    half_time_home_goals = Column(Integer)
    half_time_away_goals = Column(Integer)
    half_time_result = Column(String, nullable=True)
    home_team_goals = Column(Integer)
    away_team_goals = Column(Integer)
    full_time_result = Column(String, nullable=True)
    home_team_shots = Column(Integer, nullable=True)
    away_team_shots = Column(Integer, nullable=True)
    home_team_shots_on_target = Column(Integer, nullable=True)
    away_team_shots_on_target = Column(Integer, nullable=True)
    home_team_fouls = Column(Integer, nullable=True)
    away_team_fouls = Column(Integer, nullable=True)
    home_team_corners = Column(Integer, nullable=True)
    away_team_corners = Column(Integer, nullable=True)
    home_team_yellow_cards = Column(Integer, nullable=True)
    away_team_yellow_cards = Column(Integer, nullable=True)
    home_team_red_cards = Column(Integer, nullable=True)
    away_team_red_cards = Column(Integer, nullable=True)

    seasons = relationship("Seasons")
    home_team = relationship("Teams", foreign_keys=[home_team_id])
    away_team = relationship("Teams", foreign_keys=[away_team_id])
    referee = relationship("Referees")