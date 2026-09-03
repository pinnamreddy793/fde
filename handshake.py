import os
from dotenv import load_dotenv # type: ignore
from google import genai

load_dotenv()

api_key1 = os.getenv("GEMINIAPIKEY")
# print(api_key1)

if not api_key1:
    raise SystemExit("ERROR: GEMINIAPIKEY is not set.")

client = genai.Client(api_key=api_key1)
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Reply only with: API CONNECTED"
)
print(response.text)

# Get a custom prompt from the user
prompt = input("Enter your prompt: ")

# Send prompt to Gemini
response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=prompt
)

# Display Gemini's response
print("\nGemini Response:")
print(response.text)