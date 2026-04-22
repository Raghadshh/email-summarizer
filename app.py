import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("Email Summarizer & Chatbot")

# Email Summarizer Section
st.header("Email Summarizer")
email_input = st.text_area("Paste your email here:", height=200)

if st.button("Summarize"):
    if email_input:
        st.session_state.current_email = email_input
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an assistant that summarizes emails clearly and concisely."},
                {"role": "user", "content": f"Summarize this email: {email_input}"}
            ]
        )
        st.write(response.choices[0].message.content)

# Chatbot Section
st.header("Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_email" not in st.session_state:
    st.session_state.current_email = ""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask me anything about your email...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    system_prompt = "You are a helpful email assistant."
    if st.session_state.current_email:
        system_prompt += f" Here is the email the user is referring to: {st.session_state.current_email}"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages
        ]
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)