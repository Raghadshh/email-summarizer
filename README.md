# Mail AI

An AI powered email summarizer and chatbot built with Streamlit and Groq.

You paste an email and it gives you a summary, detects the tone, suggests a reply, and lets you chat with it.

## Features

- Summarize any email
- Tone detection (Urgent, Friendly, Formal, Angry, Neutral, Grateful)
- Suggested reply generator
- Chat with your email
- Save and switch between multiple emails
- Download your summary as a txt file

## Tech Stack

- Python
- Streamlit
- Groq API (llama-3.3-70b-versatile)
- python-dotenv

## How to run it

1. Clone the repo
2. Create a virtual environment and activate it
3. Install dependencies
4. Add your Groq API key to a `.env` file
5. Run the app

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Setup

Create a `.env` file in the root folder and add your key:
GROQ_API_KEY=your_key_here