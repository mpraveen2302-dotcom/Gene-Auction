import streamlit as st
import time
from db import load_state, save_state

st.set_page_config(layout="wide")
st.title("🎤 QUIZ MASTER DASHBOARD")

state = load_state()

# 🔄 AUTO REFRESH EVERY SECOND
time.sleep(1)
st.experimental_rerun()

# -------- ROUND SETTINGS --------
st.header("⚙️ Round Controls")
new_time = st.number_input("Countdown seconds", 3, 60, state["countdown"])

if st.button("💾 Update Timer"):
    state["countdown"] = new_time
    save_state(state)

col1, col2 = st.columns(2)

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
        state["round"] += 1
        state["game_active"] = False
        state["buzz_order"] = []
        save_state(state)

# -------- LIVE COUNTDOWN --------
st.header(f"🔴 Round {state['round']}")

if state["game_active"]:
    remaining = int(state["countdown"] - (time.time() - state["start_time"]))
    remaining = max(remaining, 0)
    st.metric("⏳ Countdown", remaining)

# -------- LEADERBOARD --------
st.header("🥇 Buzz Leaderboard")

if len(state["buzz_order"]) == 0:
    st.info("No buzzes yet")

for i, buzz in enumerate(state["buzz_order"], start=1):
    st.write(f"{i}. {buzz['team']} — {buzz['time']} sec")
