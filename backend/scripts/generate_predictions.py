import os
import sys
import pandas as pd
import xgboost as xgb
from dotenv import load_dotenv

# Add parent directory to path to import database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_supabase

load_dotenv()

from services.ai_service import generate_match_analysis

def generate_predictions_for_upcoming():
    supabase = get_supabase()
    
    # 1. Fetch upcoming matches from DB
    response = supabase.table("matches").select("*, home_team:home_team_id(name), away_team:away_team_id(name)").eq("status", "NS").execute()
    matches = response.data
    
    if not matches:
        print("No upcoming matches found in database.")
        return

    # 2. Load Model
    model_path = "backend/models/baseline_1x2.json"
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}. Please train a model first.")
        return
        
    model = xgb.XGBClassifier()
    model.load_model(model_path)
    
    print(f"Generating predictions and AI insights for {len(matches)} matches...")
    
    for match in matches:
        # Dummy features for demo
        dummy_features = [[12, 10, 5, 4, 6, 5]] 
        probs = model.predict_proba(dummy_features)[0]
        
        # Prepare data for AI analysis
        match_info = {
            "home_team": match['home_team']['name'],
            "away_team": match['away_team']['name'],
            "home_win_prob": round(float(probs[1]) * 100, 1),
            "draw_prob": round(float(probs[0]) * 100, 1),
            "away_win_prob": round(float(probs[2]) * 100, 1),
            "home_form": "WWDWL", # Placeholder: should be fetched from team_rolling_stats
            "away_form": "WWWWW"  # Placeholder
        }
        
        ai_insight = generate_match_analysis(match_info)
        
        prediction_data = {
            "match_id": match["id"],
            "home_win_prob": float(probs[1]),
            "draw_prob": float(probs[0]),
            "away_win_prob": float(probs[2]),
            "confidence_score": float(max(probs)),
            "ai_explanation": ai_insight
        }
        
        # Upsert prediction
        supabase.table("predictions").upsert(prediction_data).execute()
        
    print("Predictions and AI insights generated and stored.")

if __name__ == "__main__":
    generate_predictions_for_upcoming()
