-- Letbe Database Schema

-- 1. Leagues Table
create table leagues (
    id text primary key,
    name text not null,
    country text,
    logo_url text,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 2. Teams Table
create table teams (
    id text primary key,
    name text not null,
    short_name text,
    tla text, -- Three Letter Abbreviation
    logo_url text,
    league_id text references leagues(id),
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 3. Matches Table
create table matches (
    id text primary key,
    league_id text references leagues(id),
    home_team_id text references teams(id),
    away_team_id text references teams(id),
    match_date timestamp with time zone not null,
    status text default 'SCHEDULED', -- SCHEDULED, LIVE, FINISHED, CANCELLED
    season int,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 4. Match Statistics (Post-match data for training)
create table match_stats (
    match_id text primary key references matches(id) on delete cascade,
    home_goals int,
    away_goals int,
    home_possession int, -- Percentage
    away_possession int,
    home_shots_on_target int,
    away_shots_on_target int,
    home_corners int,
    away_corners int,
    home_yellow_cards int,
    away_yellow_cards int,
    home_red_cards int,
    away_red_cards int,
    btts boolean generated always as (home_goals > 0 and away_goals > 0) stored,
    total_goals int generated always as (home_goals + away_goals) stored,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 5. Predictions Table
create table predictions (
    id uuid default gen_random_uuid() primary key,
    match_id text unique references matches(id) on delete cascade,
    
    -- 1X2 Probabilities
    home_win_prob numeric(5,4), -- e.g., 0.6543
    draw_prob numeric(5,4),
    away_win_prob numeric(5,4),
    
    -- Market Probabilities
    btts_yes_prob numeric(5,4),
    over_25_prob numeric(5,4),
    under_25_prob numeric(5,4),
    
    -- Poisson/Regression Outputs
    predicted_home_goals numeric(3,2),
    predicted_away_goals numeric(3,2),
    predicted_corners numeric(4,2),
    predicted_yellow_cards numeric(4,2),
    
    -- Insight & Confidence
    confidence_score numeric(3,2), -- 0.0 to 1.0
    ai_explanation text, -- LLM generated commentary
    
    model_version text,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 6. Team Rolling Stats (Cached features for inference)
create table team_rolling_stats (
    team_id text references teams(id) on delete cascade,
    league_id text references leagues(id),
    avg_goals_scored_last_5 numeric(4,2),
    avg_goals_conceded_last_5 numeric(4,2),
    avg_corners_last_5 numeric(4,2),
    avg_cards_last_5 numeric(4,2),
    elo_rating int,
    updated_at timestamp with time zone default timezone('utc'::text, now()) not null,
    primary key (team_id)
);
