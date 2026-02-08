import streamlit as st
import time

st.set_page_config(page_title="Quiz Buzzer", layout="centered")

COUNTDOWN = 10  # seconds

# ---------- Session State ----------
if "game_active" not in st.session_state:
    st.session_state.game_active = False
    st.session_state.start_time = None
    st.session_state.winner = None
    st.session_state.click_time = None
    st.session_state.buzzed_teams = set()

st.title("🚨 Quiz Buzzer System")

# ---------- Team Entry ----------
team_name = st.text_input("Enter your Team Name")

# ---------- Host Controls ----------
st.divider()
col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Start"):
        st.session_state.game_active = True
        st.session_state.start_time = time.time()
        st.session_state.winner = None
        st.session_state.click_time = None
        st.session_state.buzzed_teams = set()

with col2:
    if st.button("🔁 Reset"):
        st.session_state.game_active = False
        st.session_state.start_time = None
        st.session_state.winner = None
        st.session_state.click_time = None
        st.session_state.buzzed_teams = set()

# ---------- Countdown Timer ----------
if st.session_state.game_active:
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(COUNTDOWN - elapsed, 0)

    st.subheader(f"⏳ Time Remaining: {remaining} seconds")

    if remaining == 0 and st.session_state.winner is None:
        st.warning("⏰ Time's up! No team buzzed.")
        st.session_state.game_active = False

# ---------- Buzzer ----------
st.divider()
buzz_disabled = (
    not team_name
    or not st.session_state.game_active
    or st.session_state.winner is not None
    or team_name in st.session_state.buzzed_teams
)

if st.button("🚨 BUZZ!", disabled=buzz_disabled):
    if st.session_state.winner is None:
        st.session_state.winner = team_name
        st.session_state.click_time = round(
            time.time() - st.session_state.start_time, 3
        )
        st.session_state.game_active = False
        st.session_state.buzzed_teams.add(team_name)

# ---------- Result ----------
if st.session_state.winner:
    st.success(
        f"🏆 **{st.session_state.winner} buzzed first!**\n\n"
        f"⏱ Time: {st.session_state.click_time} seconds"
    )
    st.audio(
        "https://www.soundjay.com/buttons/sounds/button-3.mp3",
        autoplay=True
    )

if team_name in st.session_state.buzzed_teams and st.session_state.winner != team_name:
    st.warning("❌ You already buzzed!")

