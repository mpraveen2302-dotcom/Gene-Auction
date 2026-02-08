import json, os

DB_FILE = "game_state.json"

default_state = {
    "round": 1,
    "game_active": False,
    "start_time": None,
    "countdown": 10,
    "buzz_order": [],
    "leaderboard": {}
}

def load_state():
    if not os.path.exists(DB_FILE):
        save_state(default_state)
        return default_state

    with open(DB_FILE, "r") as f:
        state = json.load(f)

    # Auto add missing keys (prevents crashes forever)
    for key, value in default_state.items():
        if key not in state:
            state[key] = value

    save_state(state)
    return state

def save_state(state):
    with open(DB_FILE, "w") as f:
        json.dump(state, f)
