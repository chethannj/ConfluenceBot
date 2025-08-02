import os
import streamlit as st
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load secrets
load_dotenv()

# Environment variables
BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
USERNAME = os.getenv("CONFLUENCE_USERNAME")
API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

def fetch_page_content(page_id):
    url = f"{BASE_URL}/rest/api/content/{page_id}?expand=body.storage"
    headers = {"Accept": "application/json"}
    auth = HTTPBasicAuth(USERNAME, API_TOKEN)

    response = requests.get(url, headers=headers, auth=auth)

    if response.status_code != 200:
        raise Exception(f"Confluence Error {response.status_code}: {response.text[:300]}")

    return response.json()["body"]["storage"]["value"]

def query_groq_llm(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 1000
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Groq API Error {response.status_code}: {response.text[:300]}")

    return response.json()["choices"][0]["message"]["content"]

def build_prompt(question, confluence_html):
    return f"""
You are a QA automation assistant. Use the following Confluence content to answer the user's question.

<confluence>
{confluence_html}
</confluence>

User Question: {question}

Answer:"""

# -------- Streamlit UI --------
st.set_page_config(page_title="QA Assistant for Confluence")
st.title("🧠 Confluence QA Assistant")
st.markdown("Ask questions about a Confluence page.")

page_id = st.text_input("🔢 Confluence Page ID", placeholder="e.g., 131247")
question = st.text_area("💬 Your Question", placeholder="e.g., What is the problem statement?")

if st.button("Ask"):
    if not page_id or not question:
        st.warning("Please enter both a page ID and your question.")
    else:
        try:
            with st.spinner("Fetching Confluence content..."):
                page_html = fetch_page_content(page_id)

            with st.spinner("Querying Groq..."):
                prompt = build_prompt(question, page_html)
                answer = query_groq_llm(prompt)

            st.success("✅ Answer:")
            st.write(answer)

        except Exception as e:
            st.error(f"❌ {str(e)}")
