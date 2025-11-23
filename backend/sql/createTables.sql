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
    PRIMARY KEY (team_id, season_id),
    FOREIGN KEY (team_id) REFERENCES Teams(team_id),
    FOREIGN KEY (season_id) REFERENCES Seasons(season_id)
);

-- Players (basic info only, constant data)
CREATE TABLE IF NOT EXISTS Players (
    player_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    date_of_birth DATE NOT NULL
);

-- Players in Seasons + Teams (player’s changing data)
CREATE TABLE IF NOT EXISTS Players_has_Seasons (
    player_id INT NOT NULL,
    season_id INT NOT NULL,
    team_id INT NOT NULL,
    appearances INT DEFAULT 0,
    goals INT DEFAULT 0,
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

    FOREIGN KEY (season_id) REFERENCES Seasons(season_id),
    FOREIGN KEY (referee_id) REFERENCES referees(referee_id),
    FOREIGN KEY (home_team_id) REFERENCES Teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES Teams(team_id)
);
