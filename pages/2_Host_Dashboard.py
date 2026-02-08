import streamlit as st
import time
from db import load_state, save_state

st.set_page_config(layout="wide")
st.title("🎤 QUIZ MASTER DASHBOARD")

# 🔐 PASSWORD
HOST_PASSWORD = "REC_QUIZ_2026"

password = st.text_input("Enter Host Password", type="password")
if password != HOST_PASSWORD:
    st.stop()

# Auto refresh
st.markdown("<meta http-equiv='refresh' content='1'>", unsafe_allow_html=True)

state = load_state()

def update_scores():
    points = [10,5,3,1,1,1]
    for i, buzz in enumerate(state["buzz_order"]):
        team = buzz["team"]
        score = points[i] if i < len(points) else 1
        state["leaderboard"][team] = state["leaderboard"].get(team, 0) + score
    save_state(state)

st.header("⚙️ Round Controls")

new_time = st.number_input("Countdown seconds", 3, 60, state["countdown"])

if st.button("💾 Update Timer"):
    state["countdown"] = new_time
    save_state(state)

col1, col2 = st.columns(2)

with col1:
    if st.button("▶ START ROUND"):
        state["game_active"] = True
        state["start_time"] = time.time()
        state["buzz_order"] = []
        save_state(state)

with col2:
    if st.button("⏭ NEXT ROUND"):
        update_scores()
        state["round"] += 1
        state["game_active"] = False
        state["buzz_order"] = []
        save_state(state)

st.header(f"Round {state['round']}")

if state["game_active"]:
    remaining = int(state["countdown"] - (time.time() - state["start_time"]))
    remaining = max(remaining, 0)
    st.metric("⏳ Countdown", remaining)

st.header("🏆 Leaderboard")
for team, score in sorted(state["leaderboard"].items(), key=lambda x: x[1], reverse=True):
    st.write(team, score)
