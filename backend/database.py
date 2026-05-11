import os
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

_ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=False)

_supabase: Client | None = None

def get_supabase():
    global _supabase

    if _supabase is not None:
        return _supabase

    url: str | None = os.environ.get("SUPABASE_URL")
    key: str | None = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise ValueError(
            f"SUPABASE_URL and SUPABASE_KEY must be set. Create '{_ENV_PATH}' (see '.env.example')."
        )

    _supabase = create_client(url, key)
    return _supabase
