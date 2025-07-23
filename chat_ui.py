import streamlit as st
import requests

st.set_page_config(page_title="Mental Health Bot", page_icon="💬")
st.title("🧠 Mental Health Support Bot")

# Session state to hold chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

# Input box
question = st.text_input("Ask something...", key="user_input")

# Send button
if st.button("Send") and question.strip():
    st.session_state.chat.append(("user", question))

    try:
        # Replace with your actual Flask endpoint
        res = requests.post("http://localhost:5000/api/query", json={"question": question})
        answer = res.json().get("answer", "No answer received.")
    except Exception as e:
        answer = f"❌ Error: {e}"

    st.session_state.chat.append(("bot", answer))

# Display chat messages
for sender, msg in st.session_state.chat:
    if sender == "user":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 Bot:** {msg}")
