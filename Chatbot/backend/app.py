from flask import Flask, request, jsonify
from flask_cors import CORS
from llm import get_llm_reply

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "✅ Backend running successfully"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"reply": "Please enter a message"})

    reply = get_llm_reply(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
