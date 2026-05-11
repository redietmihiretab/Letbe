import requests
import os
from dotenv import load_dotenv
from pathlib import Path

try:
    from backend.database import get_supabase
except ModuleNotFoundError:
    from database import get_supabase

_ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=False)

RAPID_API_KEY = os.environ.get("RAPID_API_KEY")
API_HOST = "api-football-v1.p.rapidapi.com"
BASE_URL = f"https://{API_HOST}/v3"

def fetch_upcoming_matches(league_id: int, season: int):
    if not RAPID_API_KEY or RAPID_API_KEY == "your_rapidapi_key":
        print("Error: RAPID_API_KEY not set in .env")
        return None

    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    
    url = f"{BASE_URL}/fixtures"
    params = {
        "league": league_id,
        "season": season,
        "next": 10 # Fetch next 10 matches
    }
    
    print(f"Fetching upcoming matches for league {league_id}...")
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json().get("response", [])
    else:
        print(f"Failed to fetch fixtures: {response.text}")
        return None

def store_matches(matches):
    supabase = get_supabase()
    
    print(f"Storing {len(matches)} matches in Supabase...")
    for match in matches:
        fixture = match["fixture"]
        teams = match["teams"]
        league = match["league"]
        
        # 1. Ensure Teams exist (Upsert)
        for team_type in ["home", "away"]:
            team_data = {
                "id": str(teams[team_type]["id"]),
                "name": teams[team_type]["name"],
                "logo_url": teams[team_type]["logo"],
                "league_id": str(league["id"])
            }
            supabase.table("teams").upsert(team_data).execute()
        
        # 2. Store Match
        match_data = {
            "id": str(fixture["id"]),
            "league_id": str(league["id"]),
            "home_team_id": str(teams["home"]["id"]),
            "away_team_id": str(teams["away"]["id"]),
            "match_date": fixture["date"],
            "status": fixture["status"]["short"],
            "season": league["season"]
        }
        supabase.table("matches").upsert(match_data).execute()
        
    print("Matches stored successfully.")

if __name__ == "__main__":
    # Premier League (39) 2023 Season (or current)
    # Note: league_id varies by API provider, 39 is standard for PL in API-Football
    live_matches = fetch_upcoming_matches(39, 2023) 
    if live_matches:
        store_matches(live_matches)
