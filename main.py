import streamlit as st
import time

st.set_page_config(page_title="Host Panel", layout="centered")

COUNTDOWN = 10

if "game_active" not in st.session_state:
    st.session_state.game_active = False
    st.session_state.start_time = None
    st.session_state.winner = None
    st.session_state.click_time = None

st.title("🎤 Quiz Host Panel")

# Start buzzer
if st.button("▶ Start Buzzer"):
    st.session_state.game_active = True
    st.session_state.start_time = time.time()
    st.session_state.winner = None
    st.session_state.click_time = None

# Reset
if st.button("🔁 Reset"):
    st.session_state.game_active = False
    st.session_state.start_time = None
    st.session_state.winner = None
    st.session_state.click_time = None

# Countdown
if st.session_state.game_active:
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(COUNTDOWN - elapsed, 0)
    st.subheader(f"⏳ Time Left: {remaining}s")

    if remaining == 0 and st.session_state.winner is None:
        st.warning("⏰ No team buzzed!")
        st.session_state.game_active = False

# Winner display
if st.session_state.winner:
    st.success(f"🏆 {st.session_state.winner} won!")
    st.info(f"⏱ Response time: {st.session_state.click_time}s")
    st.audio(
        "https://www.soundjay.com/buttons/sounds/button-3.mp3",
        autoplay=True
    )
