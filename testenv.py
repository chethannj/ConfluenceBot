import os
from dotenv import load_dotenv

load_dotenv()

print("Confluence Base URL:", os.getenv("CONFLUENCE_BASE_URL"))
print("Groq API Key Present:", bool(os.getenv("GROQ_API_KEY")))