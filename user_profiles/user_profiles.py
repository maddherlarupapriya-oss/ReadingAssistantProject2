import json
import os
from config.config import PROFILE_FILE

def load_profile():
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {"voice": "en-US-AriaNeural", "rate": "+0%"}

def save_profile(prefs):
    with open(PROFILE_FILE, "w") as f:
        json.dump(prefs, f)
