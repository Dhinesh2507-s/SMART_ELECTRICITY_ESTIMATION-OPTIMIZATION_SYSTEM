from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# 🔥 Paste your key here
GEMINI_API_KEY = "AIzaSyCPp24HwhELOBhVrnP5UAluHF_bLrS6aBs"

genai.configure(api_key=GEMINI_API_KEY)

# ✅ Updated model name
model = genai.GenerativeModel("gemini-1.5-flash")


@app.route("/")
def home():
    return "✅ Gemini Backend Running!"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"reply": "⚠️ Empty message received!"})

    try:
        response = model.generate_content(user_message)
        return jsonify({"reply": response.text})

    except Exception as e:
        return jsonify({"reply": f"⚠️ Error: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)
