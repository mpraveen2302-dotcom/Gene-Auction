import streamlit as st
import time

st.set_page_config(page_title="Team Buzzer", layout="centered")

st.title("🔘 Team Buzzer")

team_name = st.text_input("Enter your Team Name")

if not team_name:
    st.stop()

# Prevent multiple buzzes per team
if "has_buzzed" not in st.session_state:
    st.session_state.has_buzzed = False

if "game_active" not in st.session_state:
    st.info("⏳ Waiting for host to start...")
    st.stop()

disabled = (
    not st.session_state.game_active
    or st.session_state.winner is not None
    or st.session_state.has_buzzed
)

if st.button("🚨 BUZZ!", disabled=disabled):
    if st.session_state.winner is None:
        st.session_state.winner = team_name
        st.session_state.click_time = round(
            time.time() - st.session_state.start_time, 3
        )
        st.session_state.game_active = False
        st.session_state.has_buzzed = True

if st.session_state.has_buzzed:
    st.warning("❌ You have already buzzed!")

if st.session_state.winner:
    st.success(f"Winner: {st.session_state.winner}")
