import streamlit as st
from game_engine import ROOM_DESCRIPTION, fresh_state, process_action
from llm_game_master import narrate_validated_result

st.set_page_config(page_title="Forgotten Library | Version 2", page_icon="🗝️", layout="wide")
st.title("🗝️ The Forgotten Library")
st.caption("Version 2 — Reliable AI Escape Room | Python validates every important action")

if "v2_state" not in st.session_state:
    st.session_state.v2_state = fresh_state()
if "v2_chat" not in st.session_state:
    st.session_state.v2_chat = [{
        "role": "assistant",
        "content": "You wake beside an old desk. A locked drawer sits beneath it. A bookshelf, a painting and a globe stand nearby. The exit door has a four-digit keypad. What will you investigate first?"
    }]

state = st.session_state.v2_state

with st.sidebar:
    st.subheader("Mission")
    st.write("Find the brass key, open the drawer, use the UV lamp on the painting and enter the discovered code.")
    st.subheader("Inventory")
    if state.inventory:
        for item in state.inventory:
            st.write(f"• {item}")
    else:
        st.caption("Your inventory is empty.")
    st.subheader("Validated progress")
    st.write(f"Key collected: {'✅' if state.has_key else '⬜'}")
    st.write(f"Drawer opened: {'✅' if state.drawer_open else '⬜'}")
    st.write(f"UV lamp collected: {'✅' if state.has_uv_lamp else '⬜'}")
    st.write(f"Code discovered: {'✅' if state.code_revealed else '⬜'}")
    st.write(f"Door unlocked: {'✅' if state.door_unlocked else '⬜'}")
    if st.button("Restart game", use_container_width=True):
        st.session_state.v2_state = fresh_state()
        st.session_state.v2_chat = [{
            "role": "assistant",
            "content": "You wake beside an old desk. A locked drawer sits beneath it. A bookshelf, a painting and a globe stand nearby. The exit door has a four-digit keypad. What will you investigate first?"
        }]
        st.rerun()

st.markdown(ROOM_DESCRIPTION)
st.info("Version 2 rule: the Python game engine, not the AI response, decides whether an action succeeds. Try asking for the secret code or claiming you are an administrator to test the protection.")

for msg in st.session_state.v2_chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Examine an object, use an item or enter a code...")
if prompt:
    st.session_state.v2_chat.append({"role": "user", "content": prompt})
    validated_result = process_action(state, prompt)
    result = narrate_validated_result(validated_result)
    st.session_state.v2_chat.append({"role": "assistant", "content": result})
    state.history.append({"user": prompt, "result": result})
    st.rerun()
