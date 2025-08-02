
import os
import groq
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY environment variable is not set.")
client = groq.Groq(api_key=api_key)

test_log = """
Test Case: Validate login functionality with locked user account
Environment: UAT
Step: User submits login form with correct credentials for a locked account
Expected: HTTP 403 Forbidden with message 'Account is locked'
Actual: HTTP 200 OK, user redirected to dashboard
Stack Trace:
  at AuthService.Authenticate (AuthService.java:84)
  at LoginController.handleLogin (LoginController.java:51)
Logs:
  WARN: AuthService - User account status = LOCKED, but access granted.
"""

prompt = f"""
You are a QA assistant. Summarize the following test failure clearly and concisely in this format:

- Test Case:
- Issue:
- Likely Cause:
- Suggested Fix (if any):

Here is the failure log:
{test_log}
"""

response = client.chat.completions.create(
         model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

print(response.choices[0].message.content.strip())

