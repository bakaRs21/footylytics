-- Teams
CREATE TABLE IF NOT EXISTS Teams (
    team_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- Referees
CREATE TABLE IF NOT EXISTS referees (
    referee_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Seasons
CREATE TABLE IF NOT EXISTS Seasons (
    season_id SERIAL PRIMARY KEY,
    season VARCHAR(20) UNIQUE
);

-- Teams <--> Seasons (many-to-many)
CREATE TABLE IF NOT EXISTS Teams_has_Seasons (
    team_id INT NOT NULL,
    season_id INT NOT NULL,
    standing_position INT,
    wins INT,
    losses INT,
    draws INT,
    total_yel_card INT NULL,
    total_red_card INT NULL,
    total_shots_att INT NULL,
    on_target_shots INT NULL,
    hit_woodwork INT NULL,
    att_header_goal INT NULL,
    att_pen_goal INT NULL,
    att_freekick_goal INT NULL,
    att_in_box_goal INT NULL,
    att_out_box_goal INT NULL,
    goal_fastbreak  INT NULL,
    total_offsides INT NULL,
    clean_sheet INT NULL,
    goals_conceded INT NULL,
    saves INT NULL,
    outfielder_block INT NULL,
    intercpetion INT NULL,
    total_tackles INT NULL,
    last_man_tackle INT NULL,
    total_clearance INT NULL,
    head_clearance INT NULL,
    own_goals INT NULL,
    penalty_conceded INT NULL,
    pen_goals_conceded INT NULL,
    total_passes INT NULL,
    total_through_ball INT NULL,
    total_long_ball INT NULL,
    backward_pass INT NULL,
    total_cross INT NULL,
    corners_taken INT NULL,
    touches INT NULL,
    big_chance_missed INT NULL,
    clearance_off_line INT NULL,
    disposessed INT NULL,
    penalty_saved INT NULL,
    total_high_claim INT NULL,
    punches INT NULL,
    PRIMARY KEY (team_id, season_id),
    FOREIGN KEY (team_id) REFERENCES Teams(team_id),
    FOREIGN KEY (season_id) REFERENCES Seasons(season_id)
);

-- Players (basic info only, constant data)
CREATE TABLE IF NOT EXISTS Players (
    player_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL,
    foot VARCHAR(10) NOT NULL,
    height_in_meters FLOAT NOT NULL,
    nationality VARCHAR(100) NOT NULL
);

-- Players in Seasons + Teams (player’s changing data)
CREATE TABLE IF NOT EXISTS Players_has_Seasons (
    player_id INT NOT NULL,
    season_id INT NOT NULL,
    team_id INT NOT NULL,
    market_value VARCHAR(45) NULL,
    position VARCHAR(45) NULL,
    signed_from VARCHAR(45) NULL,
    jersey_number INT NULL,
    appearances INT NULL,
    wins INT NULL,
    losses INT NULL,
    goals INT NULL,
    goals_per_match FLOAT NULL,
    header_goals INT NULL,
    right_foot_goals INT NULL,
    left_foot_goals INT NULL,
    penalties_scored INT NULL,
    freekicks_scored INT NULL,
    shots INT NULL,
    shots_on_target INT NULL,
    hit_woodwork INT NULL,
    big_chanes_missed INT NULL,
    clean_sheets INT NULL,
    goals_conceded INT NULL,
    tackles INT NULL,
    last_man_tackles INT NULL,
    blocked_shots INT NULL,
    interceptions INT NULL,
    clearances INT NULL,
    header_clearance INT NULL,
    recoveries INT NULL,
    duels_won INT NULL,
    duels_lost INT NULL,
    aerial_battles_won INT NULL,
    aerial_battles_lost INT NULL,
    own_goals INT NULL,
    errors_leading_to_goal INT NULL,
    assists INT NULL,
    passes INT NULL,
    big_chances_created INT NULL,
    crosses INT NULL,
    through_balls INT NULL,
    accurate_long_balls INT NULL,
    saves INT NULL,
    penalties_saved INT NULL,
    punches INT NULL,
    high_claims INT NULL,
    catches INT NULL,
    throw_outs INT NULL,
    goal_kicks INT NULL,
    yellow_cards INT NULL,
    red_cards INT NULL,
    fouls INT NULL,
    offsides INT NULL,

    PRIMARY KEY (player_id, season_id),
    FOREIGN KEY (player_id) REFERENCES Players(player_id),
    FOREIGN KEY (season_id) REFERENCES Seasons(season_id),
    FOREIGN KEY (team_id) REFERENCES Teams(team_id)
);

-- Matches
CREATE TABLE IF NOT EXISTS matches (
    match_id SERIAL PRIMARY KEY,
    season_id INT NOT NULL,
    referee_id INT NOT NULL,
    home_team_id INT NOT NULL,
    away_team_id INT NOT NULL,
    match_date DATE NOT NULL,
    half_time_home_goals INT NULL,
    half_time_away_goals INT NULL,
    half_time_result VARCHAR(10) NULL,
    full_time_home_goals INT NULL,
    full_time_away_goals INT NULL,
    full_time_result VARCHAR(10) NULL,
    home_team_shots INT NULL,
    away_team_shots INT NULL,
    home_team_shots_on_target INT NULL,
    away_team_shots_on_target INT NULL,
    home_team_fouls INT NULL,
    away_team_fouls INT NULL,
    home_team_corners INT NULL,
    away_team_corners INT NULL,
    home_team_yellow_cards INT NULL,
    away_team_yellow_cards INT NULL,
    home_team_red_cards INT NULL,
    away_team_red_cards INT NULL,

    FOREIGN KEY (season_id) REFERENCES Seasons(season_id),
    FOREIGN KEY (referee_id) REFERENCES referees(referee_id),
    FOREIGN KEY (home_team_id) REFERENCES Teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES Teams(team_id)
);
