from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Letbe AI Prediction API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from database import get_supabase

supabase = get_supabase()

@app.get("/api/v1/predictions")
async def get_all_predictions():
    # Fetch predictions joined with match and team data
    response = supabase.table("predictions").select("""
        *,
        matches (
            match_date,
            home_team:home_team_id(name, logo_url),
            away_team:away_team_id(name, logo_url)
        )
    """).execute()
    
    return {"data": response.data}

@app.get("/predictions/{match_id}")
async def get_prediction(match_id: str):
    response = supabase.table("predictions").select("*").eq("match_id", match_id).single().execute()
    return response.data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
