from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=False)

app = FastAPI(title="Letbe AI Prediction API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    # When running from repo root: `uvicorn backend.main:app`
    from backend.database import get_supabase
except ModuleNotFoundError:
    # When Render "Root Directory" is `backend`: `uvicorn main:app`
    from database import get_supabase

@app.get("/")
async def root():
    return {"message": "Letbe AI Backend is LIVE", "status": "healthy"}

@app.get("/api/v1/predictions")
async def get_all_predictions():
    # Fetch predictions joined with match and team data
    try:
        supabase = get_supabase()
        response = supabase.table("predictions").select("""
            *,
            matches (
                match_date,
                home_team:home_team_id(name, logo_url),
                away_team:away_team_id(name, logo_url)
            )
        """).execute()
        return {"data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/predictions/{match_id}")
async def get_prediction(match_id: str):
    try:
        supabase = get_supabase()
        response = supabase.table("predictions").select("*").eq("match_id", match_id).single().execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
