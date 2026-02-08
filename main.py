import streamlit as st
import time
from db import load_state, save_state

st.set_page_config(layout="wide")
st.title("🎤 QUIZ MASTER DASHBOARD")

state = load_state()

# ---------- AUTO REFRESH ----------
time.sleep(1)
st.rerun()

# ---------- SCORING FUNCTION ----------
def update_scores():
    points = [10,5,3,1,1,1]
    for i, buzz in enumerate(state["buzz_order"]):
        team = buzz["team"]
        score = points[i] if i < len(points) else 1
        state["leaderboard"][team] = state["leaderboard"].get(team, 0) + score
    save_state(state)

# ---------- ROUND CONTROLS ----------
st.header("⚙️ Round Controls")

new_time = st.number_input("Countdown seconds", 3, 60, state["countdown"])

if st.button("💾 Update Timer"):
    state["countdown"] = new_time
    save_state(state)

col1, col2, col3 = st.columns(3)

# START ROUND
with col1:
    if st.button("▶ START ROUND"):
        state["game_active"] = True
        state["start_time"] = time.time()
        state["buzz_order"] = []
        save_state(state)

# NEXT ROUND
with col2:
    if st.button("⏭ NEXT ROUND"):
        update_scores()
        state["round"] += 1
        state["game_active"] = False
        state["buzz_order"] = []
        save_state(state)

# RESET GAME
with col3:
    if st.button("🔁 RESET GAME"):
        state = {
            "round": 1,
            "game_active": False,
            "start_time": None,
            "countdown": 10,
            "buzz_order": [],
            "leaderboard": {}
        }
        save_state(state)

# ---------- LIVE ROUND STATUS ----------
st.header(f"🔴 Round {state['round']}")

if state["game_active"]:
    remaining = int(state["countdown"] - (time.time() - state["start_time"]))
    remaining = max(remaining, 0)
    st.metric("⏳ Countdown", remaining)

# ---------- ROUND BUZZ ORDER ----------
st.subheader("🥇 Round Buzz Order")

if len(state["buzz_order"]) == 0:
    st.info("No buzzes yet")

for i, buzz in enumerate(state["buzz_order"], start=1):
    st.write(f"{i}. {buzz['team']} — {buzz['time']} sec")

# ---------- OVERALL LEADERBOARD ----------
st.header("🏆 Overall Leaderboard")

sorted_board = sorted(
    state["leaderboard"].items(),
    key=lambda x: x[1],
    reverse=True
)

if len(sorted_board) == 0:
    st.info("No scores yet")

for i, (team, score) in enumerate(sorted_board, start=1):
    st.write(f"{i}. {team} — {score} pts")
