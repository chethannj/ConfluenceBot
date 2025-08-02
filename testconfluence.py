import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
EMAIL = os.getenv("CONFLUENCE_USERNAME")
API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")

def test_api():
    url = f"{BASE_URL}/rest/api/space"
    auth = HTTPBasicAuth(EMAIL, API_TOKEN)
    r = requests.get(url, auth=auth)

    if r.status_code == 200:
        print("✅ API access confirmed!")
    else:
        print(f"❌ API failed: {r.status_code}")
        print(r.text)

test_api()
