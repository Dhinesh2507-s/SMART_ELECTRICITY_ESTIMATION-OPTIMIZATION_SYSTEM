import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY not found in .env")

# Configure Gemini
genai.configure(api_key=API_KEY)

# Load model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "You are an electricity and energy assistant. "
        "Answer ONLY questions related to electricity usage, appliances, "
        "power consumption, electricity bills, and energy saving. "
        "If the question is unrelated, say: "
        "'I can only help with electricity and energy related questions.'"
    )
)

def get_llm_reply(user_message: str) -> str:
    try:
        response = model.generate_content(user_message)
        return response.text.strip()
    except Exception as e:
        print("❌ Gemini SDK error:", e)
        return "⚠️ Error contacting AI service"
