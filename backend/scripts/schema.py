from pydantic import BaseModel
from sqlalchemy import Integer

class Seasons(BaseModel):
    season: str
    class Config:
        orm_mode = True
class Teams(BaseModel):
    name: str
    class Config:
        orm_mode = True
class Referees(BaseModel):
    name: str
    class Config:
        orm_mode = True

class Players(BaseModel):
    name: str
    date_of_birth: str
    foot: str | None = None
    height_in_meters: float | None
    nationality: str
    class Config:
        orm_mode = True

class TeamHasSeason(BaseModel):
    team_id: int
    season_id: int
    standing_position: int
    wins: int
    losses: int
    draws: int
    total_yel_card: int | None = None
    total_red_card: int | None = None
    total_shots_att: int | None = None
    on_target_shots: int | None = None
    hit_woodwork: int | None = None
    att_header_goal: int | None = None
    att_pen_goal: int | None = None
    att_freekick_goal: int | None = None
    att_in_box_goal: int | None = None
    att_out_box_goal: int | None = None
    goal_fastbreak: int | None = None
    total_offsides: int | None = None
    clean_sheet: int | None = None
    goals_conceded: int | None = None
    saves: int | None = None
    outfielder_block: int | None = None
    intercpetion: int | None = None
    total_tackles: int | None = None
    last_man_tackle: int | None = None
    total_clearances: int | None = None
    head_clearance: int | None = None
    own_goals: int | None = None
    penalty_conceded: int | None = None
    pen_goals_conceded: int | None = None
    total_passes: int | None = None
    total_through_ball: int | None = None
    total_long_ball: int | None = None
    backward_pass: int | None = None
    total_cross: int | None = None
    corners_taken: int | None = None
    touches: int | None = None
    big_chance_missed: int | None = None
    clearance_off_line: int | None = None
    dispossessed: int | None = None
    penalty_saved: int | None = None
    total_high_claim: int | None = None
    punches: int | None = None

    class Config:
        orm_mode = True

class PlayerHasSeasons(BaseModel):
    player_id: int
    season_id: int
    team_id: int
    market_value: str | None = None
    position: str | None = None
    signed_from: str | None = None
    jersey_number: int | None = None
    appearances: int | None = None
    wins: int | None = None
    losses: int | None = None
    draws: int | None = None
    goals_per_match: float | None = None
    header_goals: int | None = None
    right_foot_goals: int | None = None
    left_foot_goals: int | None = None
    pen_goals: int | None = None
    freekick_goals: int | None = None
    shots_total: int | None = None
    shots_on_target: int | None = None
    hit_woodwork: int | None = None
    big_chances_missed: int | None = None
    clean_sheets: int | None = None
    goals_conceded: int | None = None
    tackles: int | None = None
    last_man_tackles: int | None = None
    blocked_shots: int | None = None
    clearances: int | None = None
    header_clearances: int | None = None
    interceptions: int | None = None
    recoveries: int | None = None
    duels_won: int | None = None
    duels_lost: int | None = None
    aerial_battles_won: int | None = None
    aerial_battles_lost: int | None = None
    own_goals: int | None = None
    errors_leading_to_goal: int | None = None
    assists: int | None = None
    passes_total: int | None = None
    big_chances_created: int | None = None
    crosses_total: int | None = None
    through_balls: int | None = None
    accurate_long_balls: int | None = None
    saves: int | None = None
    penalties_saved: int | None = None
    punches: int | None = None
    high_claims: int | None = None
    catches: int | None = None
    throw_outs: int | None = None
    goal_kicks: int | None = None
    yellow_cards: int | None = None
    red_cards: int | None = None
    fouls_committed: int | None = None
    offsides: int | None = None

    class Config:
        orm_mode = True

class AllMatches(BaseModel):
    season_id: int
    referee_id: int
    date: str
    home_team_id: int
    away_team_id: int
    half_time_home_goals: int
    half_time_away_goals: int
    half_time_result: str | None = None
    home_team_goals: int
    away_team_goals: int
    full_time_result: str | None = None
    home_team_shots: int | None = None
    away_team_shots: int | None = None
    home_team_shots_on_target: int | None = None
    away_team_shots_on_target: int | None = None
    home_team_fouls: int | None = None
    away_team_fouls: int | None = None
    home_team_corners: int | None = None
    away_team_corners: int | None = None
    home_team_yellow_cards: int | None = None
    away_team_yellow_cards: int | None = None
    home_team_red_cards: int | None = None
    away_team_red_cards: int | None = None

    class Config:
        orm_mode = True