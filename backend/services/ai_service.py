import google.generativeai as genai
import os
from pathlib import Path
from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=False)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

def generate_match_analysis(match_info: dict):
    """
    match_info should contain:
    - home_team, away_team
    - home_win_prob, draw_prob, away_win_prob
    - home_form (e.g., 'WWWLD'), away_form
    - key_stats (optional)
    """
    if not model:
        return "AI analysis unavailable (GEMINI_API_KEY not set)."

    prompt = f"""
    As a professional football analyst, provide a concise (2-3 sentences) analysis for the upcoming match:
    {match_info['home_team']} vs {match_info['away_team']}.

    Model Probabilities:
    - {match_info['home_team']} Win: {match_info['home_win_prob']}%
    - Draw: {match_info['draw_prob']}%
    - {match_info['away_team']} Win: {match_info['away_win_prob']}%

    Recent Form:
    - {match_info['home_team']}: {match_info['home_form']}
    - {match_info['away_team']}: {match_info['away_form']}

    Your analysis should explain WHY the model might be favoring one side or why it predicts a tight game. 
    Use professional, engaging language.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating AI analysis: {e}")
        return "Error generating analysis. Please check your AI model parameters."

if __name__ == "__main__":
    # Test
    test_match = {
        "home_team": "Manchester City",
        "away_team": "Arsenal",
        "home_win_prob": 45,
        "draw_prob": 30,
        "away_win_prob": 25,
        "home_form": "WWDLW",
        "away_form": "WWWWW"
    }
    print(generate_match_analysis(test_match))
