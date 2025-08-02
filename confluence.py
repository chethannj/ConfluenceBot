import os
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import groq

load_dotenv()

CONFLUENCE_BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
CONFLUENCE_USERNAME = os.getenv("CONFLUENCE_USERNAME")
CONFLUENCE_API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def fetch_confluence_page(page_id):
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{page_id}?expand=body.storage"
    auth = HTTPBasicAuth(CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN)
    response = requests.get(url, auth=auth)
    response.raise_for_status()
    content = response.json()
    html_body = content["body"]["storage"]["value"]
    return BeautifulSoup(html_body, "html.parser").get_text()

def ask_confluence_question(question, page_text):
    client = groq.Groq(api_key=GROQ_API_KEY)
    prompt = f"""
You are a QA assistant. Based on this Confluence page:

--- START ---
{page_text[:8000]}
--- END ---

Question: {question}
Answer:"""
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
