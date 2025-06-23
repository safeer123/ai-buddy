import google.generativeai as genai
from dotenv import load_dotenv
from github_helper import fetch_file_from_github
import os

load_dotenv()

github_url = os.getenv("GITHUB_HR_POLICY_FILE")

# Configure Gemini with API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize model
model = genai.GenerativeModel("gemini-2.5-flash")

static_context = fetch_file_from_github(github_url)

chat = model.start_chat(history=[
    {
        "role": "user",
        "parts": [f"You are an HR assistant bot. Use the following static company policy for answering any HR-related questions:\n\n{static_context}"]
    }
])

# ✅ Hybrid Ask Function
def ask_gemini(dynamic_context: str, question: str) -> str:
    prompt = f"""
    The following is dynamic context relevant to the question:

    {dynamic_context}

    Now answer the question:
    {question}
    """
    try:
        response = chat.send_message(prompt)
        return response.text.strip()
    except Exception as e:
        print("❌ Gemini Error:", str(e))
        return "Sorry, I couldn't generate a reply."