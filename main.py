import streamlit as st
import time

st.set_page_config(page_title="Simple Buzzer", layout="centered")

COUNTDOWN = 10  # seconds

# ---- Session state ----
if "start_time" not in st.session_state:
    st.session_state.start_time = None
    st.session_state.buzzed = False

st.title("🚨 Simple Quiz Buzzer")

# ---- Start Button ----
if st.button("▶ Start Countdown"):
    st.session_state.start_time = time.time()
    st.session_state.buzzed = False

# ---- Countdown Timer ----
if st.session_state.start_time and not st.session_state.buzzed:
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(COUNTDOWN - elapsed, 0)

    st.subheader(f"⏳ Time Remaining: {remaining} seconds")

    if remaining == 0:
        st.warning("⏰ Time's up!")

# ---- Buzzer Button ----
if st.session_state.start_time:
    if st.button("🚨 BUZZ!"):
        if not st.session_state.buzzed:
            st.session_state.buzzed = True
            response_time = round(
                time.time() - st.session_state.start_time, 3
            )

            st.success(f"Buzzed at {response_time} seconds!")
            st.audio(
                "https://www.soundjay.com/buttons/sounds/button-3.mp3",
                autoplay=True
            )
