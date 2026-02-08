import json, os

DB_FILE = "game_state.json"

default_state = {
    "round": 1,
    "game_active": False,
    "start_time": None,
    "countdown": 10,
    "buzz_order": []   # ⭐ NEW
}

def load_state():
    if not os.path.exists(DB_FILE):
        save_state(default_state)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(DB_FILE, "w") as f:
        json.dump(state, f)
