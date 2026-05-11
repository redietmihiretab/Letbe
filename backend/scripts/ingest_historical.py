import pandas as pd
import requests
import os
from io import StringIO

# Configuration
# E0 = Premier League, D1 = Bundesliga, SP1 = La Liga, I1 = Serie A, F1 = Ligue 1
LEAGUES = {
    "E0": "Premier League",
    "D1": "Bundesliga",
    "SP1": "La Liga"
}
SEASONS = ["2324", "2223"]
BASE_URL = "https://www.football-data.co.uk/mmz4281/{season}/{league}.csv"

def download_data(league_code, season):
    url = BASE_URL.format(season=season, league=league_code)
    print(f"Downloading {LEAGUES[league_code]} for season {season}...")
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        print(f"Failed to download data from {url}")
        return None

def calculate_rolling_stats(df, window=5):
    """
    Calculate rolling averages for key metrics to capture team form.
    """
    df = df.sort_values('Date')
    
    metrics = {
        'FTHG': 'goals_scored',
        'FTAG': 'goals_conceded',
        'HS': 'shots',
        'HST': 'shots_on_target',
        'HC': 'corners',
        'HY': 'yellow_cards'
    }
    
    # We need to calculate this for each team as both Home and Away
    # This is a simplified version; in a full system we'd meld home/away stats
    stats_list = []
    
    for team in df['HomeTeam'].unique():
        team_matches = df[(df['HomeTeam'] == team) | (df['AwayTeam'] == team)].copy()
        
        # Calculate metric for this team regardless of if they were home or away
        # This is the "proper" way to get a team's true form
        # ... logic to calculate rolling mean ...
        pass # To be implemented in full in the script
    
    return df

def process_match_data(df):
    if df is None:
        return None
    
    # Map columns to standard names
    # FTHG = Full Time Home Goals, FTAG = Full Time Away Goals
    # HS = Home Shots, AS = Away Shots, HST = Home Shots on Target, AST = Away Shots on Target
    # HC = Home Corners, AC = Away Corners, HY = Home Yellow, AY = Away Yellow
    
    # 1. Basic Outcome Labels
    df['total_goals'] = df['FTHG'] + df['FTAG']
    df['btts'] = (df['FTHG'] > 0) & (df['FTAG'] > 0)
    
    # 2. Rolling Averages (The key to accuracy)
    # We'll calculate the last 5 matches avg for goals, shots, corners
    for team in pd.concat([df['HomeTeam'], df['AwayTeam']]).unique():
        team_mask = (df['HomeTeam'] == team) | (df['AwayTeam'] == team)
        team_df = df[team_mask].sort_values('Date')
        
        # Goals scored by this team
        team_df['goals'] = team_df.apply(lambda x: x['FTHG'] if x['HomeTeam'] == team else x['FTAG'], axis=1)
        df.loc[team_mask, f'{team}_avg_goals'] = team_df['goals'].shift(1).rolling(window=5).mean()
        
    return df

if __name__ == "__main__":
    # Example: Download Premier League 23/24
    raw_data = download_data("E0", "2324")
    if raw_data is not None:
        processed = process_match_data(raw_data)
        print("\nIngestion Preview (First 5 matches):")
        print(processed.head())
        
        # Save to local csv for now
        os.makedirs("backend/data", exist_ok=True)
        processed.to_csv("backend/data/E0_2324_processed.csv", index=False)
        print("\nData saved to backend/data/E0_2324_processed.csv")
