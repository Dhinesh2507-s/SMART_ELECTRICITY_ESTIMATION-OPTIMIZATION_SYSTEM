import os
from flask import Flask, render_template, request, jsonify
from google import genai

app = Flask(__name__)

GEMINI_API_KEY = "AIzaSyBJkO_Z8dakEbK6M8zh8Dt5nO7qtq5gIZg"
client = genai.Client(api_key=GEMINI_API_KEY)

@app.route('/')
def home_page():
    return render_template('home.html')

@app.route('/eee-bot')
def eee_feature():
    # This renders the full-page chatbot
    return render_template('index.html')

@app.route('/chat/home', methods=['POST'])
def chat_home():
    user_message = request.json.get("message")
    instruction = "You are a friendly site navigator. Guide users to the 'Electrical Bot' for technical questions."
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            config={"system_instruction": instruction},
            contents=user_message
        )
        return jsonify({"reply": response.text})
    except:
        return jsonify({"reply": "Error on home bot."})

@app.route('/chat/eee', methods=['POST'])
def chat_eee():
    user_message = request.json.get("message")
    instruction = """
    You are a specialized Professor in EEE. 
    Answer ONLY electronics and electrical engineering questions. 
    Include diagrams description or formulas where necessary.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            
            config={"system_instruction": instruction},
            contents=user_message
        )
        return jsonify({"reply": response.text})
    except:
        return jsonify({"reply": "The EEE Lab is currently closed for maintenance."})

if __name__ == '__main__':
    app.run(debug=True)