import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("Email Summarizer & Chatbot")

email_input = st.text_area("Paste your email here:", height=200)

if st.button("Summarize"):
    if email_input:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an assistant that summarizes emails clearly and concisely."},
                {"role": "user", "content": f"Summarize this email: {email_input}"}
            ]
        )
        st.write(response.choices[0].message.content)