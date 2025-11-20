-- SQL to create the main tables. Run this once (psql -f backend/sql/create_tables.sql) or let the loader run it.
-- Adjust owner/permissions as needed.

-- 1) results (clean relational table)
CREATE TABLE IF NOT EXISTS results (
  id SERIAL PRIMARY KEY,
  home_team TEXT NOT NULL,
  away_team TEXT NOT NULL,
  home_goals INTEGER,
  away_goals INTEGER,
  result CHAR(1),
  season TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 2) all_matches: store known columns if present, otherwise use staging table below
CREATE TABLE IF NOT EXISTS all_matches (
  id SERIAL PRIMARY KEY,
  match_date DATE,
  home_team TEXT,
  away_team TEXT,
  home_goals INTEGER,
  away_goals INTEGER,
  season TEXT,
  metadata JSONB,  -- keeps any other columns that are not formalized
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 3) team_stats: safe approach — keep team + jsonb for all numeric columns
CREATE TABLE IF NOT EXISTS team_stats_raw (
  id SERIAL PRIMARY KEY,
  team TEXT,
  stats JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- If you prefer a flat table you can add columns manually later; the loader stores row -> JSON.

-- 4) players (staging/raw)
CREATE TABLE IF NOT EXISTS players_raw (
  id SERIAL PRIMARY KEY,
  raw JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 5) top20 players (staging/raw)
CREATE TABLE IF NOT EXISTS top20_players_raw (
  id SERIAL PRIMARY KEY,
  raw JSONB,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 6) EPL standings normalized (team, season, position)
CREATE TABLE IF NOT EXISTS epl_standings (
  id SERIAL PRIMARY KEY,
  team TEXT NOT NULL,
  season TEXT NOT NULL,
  position INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
  UNIQUE (team, season)
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_results_season ON results (season);
CREATE INDEX IF NOT EXISTS idx_all_matches_season ON all_matches (season);
CREATE INDEX IF NOT EXISTS idx_epl_team ON epl_standings (team);