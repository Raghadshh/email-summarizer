import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="Mail AI", page_icon="logo.svg", layout="wide")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }

        .stApp {
            background-color: #080808;
            color: #e2e2e2;
        }

        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(16px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .fade-up {
            animation: fadeUp 0.5s ease forwards;
        }

        .fade-up-delay {
            animation: fadeUp 0.5s ease 0.15s forwards;
            opacity: 0;
        }

        .fade-up-delay-2 {
            animation: fadeUp 0.5s ease 0.3s forwards;
            opacity: 0;
        }

        section[data-testid="stSidebar"] {
            background-color: #0f0f0f !important;
            border-right: 1px solid #1a1a1a !important;
            padding-top: 2rem;
        }

        section[data-testid="stSidebar"] h1 {
            font-size: 1rem !important;
            color: #444 !important;
            text-transform: uppercase;
            letter-spacing: 3px;
        }

        h1 {
            font-size: 1.8rem !important;
            font-weight: 600 !important;
            color: #ffffff !important;
            letter-spacing: -0.5px;
        }

        h2, h3 {
            font-size: 0.75rem !important;
            font-weight: 500 !important;
            color: #444 !important;
            text-transform: uppercase !important;
            letter-spacing: 3px !important;
            margin-top: 2.5rem !important;
            margin-bottom: 1rem !important;
        }

        .stTextArea textarea {
            background-color: #111111 !important;
            border: 1px solid #1f1f1f !important;
            border-radius: 14px !important;
            color: #e2e2e2 !important;
            font-family: 'DM Sans', sans-serif !important;
            font-size: 0.95rem !important;
            line-height: 1.6 !important;
            padding: 1rem !important;
            transition: border-color 0.2s ease !important;
        }

        .stTextArea textarea:focus {
            border-color: #6366f1 !important;
            box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
        }

        .stButton button {
            background-color: transparent !important;
            color: #888 !important;
            border: 1px solid #1f1f1f !important;
            border-radius: 8px !important;
            font-family: 'DM Sans', sans-serif !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            padding: 0.4rem 1rem !important;
            transition: all 0.2s ease !important;
            width: 100%;
        }

        .stButton button:hover {
            border-color: #6366f1 !important;
            color: #a5b4fc !important;
            background-color: rgba(99,102,241,0.05) !important;
        }

        .primary-btn button {
            background: linear-gradient(135deg, #6366f1, #a855f7) !important;
            color: white !important;
            border: none !important;
            font-size: 0.9rem !important;
        }

        .primary-btn button:hover {
            opacity: 0.9 !important;
            color: white !important;
        }

        .stChatMessage {
            background-color: #111111 !important;
            border: 1px solid #1a1a1a !important;
            border-radius: 14px !important;
            margin-bottom: 0.75rem !important;
            animation: fadeUp 0.3s ease forwards;
        }

        .stChatInputContainer, [data-testid="stChatInput"] {
            background-color: #111111 !important;
            border: 1px solid #1f1f1f !important;
            border-radius: 14px !important;
        }

        [data-testid="stCode"] {
            background-color: #111111 !important;
            border: 1px solid #1f1f1f !important;
            border-radius: 14px !important;
        }

        [data-testid="stSelectbox"] > div > div {
            background-color: #111111 !important;
            border-color: #1f1f1f !important;
            color: #e2e2e2 !important;
            border-radius: 10px !important;
        }

        [data-testid="stAlert"] {
            background-color: #0f2a1a !important;
            border: 1px solid #166534 !important;
            border-radius: 10px !important;
        }

        hr {
            border-color: #1a1a1a !important;
            margin: 2rem 0 !important;
        }

        #MainMenu, footer, header {visibility: hidden;}

        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: #0a0a0a; }
        ::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# sidebar - shows saved emails
with st.sidebar:
    st.markdown("<h1>Mail AI</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if "saved_emails" not in st.session_state:
        st.session_state.saved_emails = {}

    if st.session_state.saved_emails:
        st.markdown("### Saved Emails")
        selected = st.selectbox("", list(st.session_state.saved_emails.keys()), label_visibility="collapsed")
        if st.button("Load Email"):
            st.session_state.current_email = st.session_state.saved_emails[selected]
            st.session_state.messages = []
            st.success("Loaded!")
    else:
        st.markdown("<p style='color:#333;font-size:0.85rem;'>No saved emails yet.</p>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<p style='color:#222;font-size:0.75rem;'>Built with Groq + Streamlit</p>", unsafe_allow_html=True)

# keep track of messages and email between reruns
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_email" not in st.session_state:
    st.session_state.current_email = ""
if "last_summary" not in st.session_state:
    st.session_state.last_summary = ""

# split the page into two columns
left, right = st.columns([1.1, 0.9], gap="large")

# left side is the email input and summary
with left:
    st.markdown("<div class='fade-up'>", unsafe_allow_html=True)
    st.markdown("<h1>Mail AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#444;margin-top:-0.5rem;margin-bottom:2rem;font-size:0.95rem;'>Paste an email. Get the point.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='fade-up-delay'>", unsafe_allow_html=True)
    st.markdown("### Email")
    email_input = st.text_area("", height=220, placeholder="Paste your email here...", label_visibility="collapsed")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='primary-btn'>", unsafe_allow_html=True)
        summarize = st.button("Summarize")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        save = st.button("Save")
    with col3:
        clear = st.button("Clear")

    if summarize and email_input:
        st.session_state.current_email = email_input
        with st.spinner(""):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an assistant that summarizes emails clearly and concisely."},
                    {"role": "user", "content": f"Summarize this email: {email_input}"}
                ]
            )
            summary = response.choices[0].message.content
            st.session_state.last_summary = summary

    if save and email_input:
        label = email_input[:30] + "..."
        st.session_state.saved_emails[label] = email_input
        st.success("Saved!")

    if clear:
        st.session_state.current_email = ""
        st.session_state.messages = []
        st.session_state.last_summary = ""
        st.rerun()

    if st.session_state.last_summary:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Summary")
        st.markdown(f"<div style='background:#111;border:1px solid #1f1f1f;border-radius:14px;padding:1.2rem 1.4rem;line-height:1.7;color:#ccc;font-size:0.95rem;animation:fadeUp 0.4s ease forwards;'>{st.session_state.last_summary}</div>", unsafe_allow_html=True)
        st.code(st.session_state.last_summary, language=None)

    st.markdown("</div>", unsafe_allow_html=True)

# right side is the chat
with right:
    st.markdown("<div class='fade-up-delay-2'>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Chat")

    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    user_input = st.chat_input("Ask about your email...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        system_prompt = "You are a helpful email assistant. Be concise and clear."
        if st.session_state.current_email:
            system_prompt += f" Here is the email the user is referring to: {st.session_state.current_email}"

        with st.spinner(""):
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

    st.markdown("</div>", unsafe_allow_html=True)