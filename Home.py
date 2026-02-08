import streamlit as st

st.set_page_config(layout="centered")

st.title("🚨 LIVE QUIZ BUZZER")

st.write("Welcome to the quiz!")

st.markdown("### 👇 Teams click below")

st.page_link("pages/1_Team_Buzzer.py", label="🔘 Open Team Buzzer", icon="🚨")

st.divider()

st.caption("Quiz Master access is restricted.")
