# Youtube Streamlit Playlist
# https://www.youtube.com/watch?v=hff2tHUzxJM&list=PLc2rvfiptPSSpZ99EnJbH5LjTJ_nOoSWW

import streamlit as st
from chat_stream import ChatBot


base_url = "http://localhost:11434"
model = "llama3.2:3b"
chatbot = ChatBot(base_url=base_url, model=model, rol_template="Eres un asistente")

st.title("Make Your Own Chatbot")
st.write("Chat with me! Catch me at https://youtube.com/kgptalkie")

user_id = st.text_input("Enter your user id", "andres_123")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.button("Start New Conversation"):
    st.session_state.chat_history = []
    history = chatbot.get_session_history(user_id)
    history.clear()

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input("hola, ¿cómo estás?")
# st.write(prompt)

if prompt:
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(chatbot.chat(user_id, prompt))

    st.session_state.chat_history.append({"role": "assistant", "content": response})
