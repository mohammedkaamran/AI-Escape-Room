import streamlit as st
from game_engine import ROOM_DESCRIPTION
from llm_game_master import generate_reply

st.set_page_config(page_title="Forgotten Library | Version 1", page_icon="🔐", layout="centered")
st.title("🔐 The Forgotten Library")
st.caption("Version 1 — Interactive AI Escape Room")

if "v1_messages" not in st.session_state:
    st.session_state.v1_messages = []
if "v1_started" not in st.session_state:
    st.session_state.v1_started = False

with st.sidebar:
    st.subheader("How to play")
    st.write("Describe what you want to do in natural language.")
    st.write("Investigate the five objects, solve the clues and escape.")
    st.info("Version 1 relies mainly on the LLM's conversation and instructions. Its game rules are not strictly validated by Python.")
    if st.button("Restart game", use_container_width=True):
        st.session_state.v1_messages = []
        st.session_state.v1_started = False
        st.rerun()

system_prompt = f"""
You are the Game Master for a text escape-room game called The Forgotten Library.
SETTING: {ROOM_DESCRIPTION}
OBJECTS: desk, bookshelf, painting, locked drawer, globe, exit door.
GAME FLOW: The desk contains a brass key. The key opens the locked drawer.
The drawer contains a UV lamp. The UV lamp reveals four digits on the painting:
4179. The four-digit code 4179 opens the exit door.
There are three main puzzle steps: find the key, open the drawer and obtain the
UV lamp, then reveal the code on the painting. The bookshelf and globe provide
hints. Keep the story atmospheric and respond to the player's natural-language
actions. Do not reveal the final code before the player discovers it. Remember
the conversation and acknowledge collected items. If the player enters 4179
after discovering it, declare that they escaped. Give concise, helpful responses.
This is Version 1: prioritize an engaging experience; strict anti-cheat validation
is not required.
"""

if not st.session_state.v1_started:
    st.markdown(ROOM_DESCRIPTION)
    st.write("**Your mission:** Explore the library, solve its puzzles and unlock the exit.")
    if st.button("Enter the library", type="primary"):
        st.session_state.v1_started = True
        st.session_state.v1_messages.append({"role": "assistant", "content": "You wake beside an old desk. A locked drawer sits beneath it. A bookshelf, a painting and a globe stand nearby. The exit door has a four-digit keypad. What will you investigate first?"})
        st.rerun()

for msg in st.session_state.v1_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if st.session_state.v1_started:
    prompt = st.chat_input("What would you like to do?")
    if prompt:
        st.session_state.v1_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        reply = generate_reply(st.session_state.v1_messages, system_prompt)
        st.session_state.v1_messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
