import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

def ask_gemini(context, question):
    prompt = f"""Answer the following HR-related question using this context:\n\n{context}\n\nQuestion: {question}"""
    response = model.generate_content(prompt)
    return response.text.strip()
