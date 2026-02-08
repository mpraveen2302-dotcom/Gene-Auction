import streamlit as st
import time
from db import load_state, save_state

st.title("🔘 TEAM BUZZER")

team = st.text_input("Enter Team Name")
state = load_state()

# ---------- AUTO REFRESH ----------
time.sleep(1)
st.rerun()

st.subheader(f"Round {state['round']}")

# ---------- LIVE COUNTDOWN ----------
if state["game_active"]:
    remaining = int(state["countdown"] - (time.time() - state["start_time"]))
    remaining = max(remaining, 0)
    st.metric("⏳ Time Left", remaining)

# ---------- BUZZ BUTTON ----------
already_buzzed = [b["team"] for b in state["buzz_order"]]

disabled = (
    not team
    or not state["game_active"]
    or team in already_buzzed
)

if st.button("🚨 BUZZ!", disabled=disabled):
    buzz_time = round(time.time() - state["start_time"], 3)

    state["buzz_order"].append({
        "team": team,
        "time": buzz_time
    })
    save_state(state)

# ---------- AUCTION BUZZER SOUND ----------
if len(state["buzz_order"]) > 0:
    st.audio(
        "https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3",
        autoplay=True
    )

# ---------- SHOW POSITION ----------
for i, buzz in enumerate(state["buzz_order"], start=1):
    if buzz["team"] == team:
        st.success(f"You buzzed #{i}!")
