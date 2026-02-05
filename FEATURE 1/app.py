from flask import Flask, render_template, request, jsonify
import pickle
from utils.suggestion_logic import generate_suggestions

app = Flask(__name__)

# ✅ Correct model path & name
model = pickle.load(open("model/electricity_model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    # ⚠️ Must match training columns order
    features = [[
        data["family_size"],
        data["num_appliances"],
        data["total_hours"],
        data["avg_condition"]
    ]]

    predicted_units = float(model.predict(features)[0])

    suggestions = generate_suggestions(
        data,
        predicted_units
    )

    return jsonify({
        "predicted_units": round(predicted_units, 2),
        "suggestions": suggestions
    })

if __name__ == "__main__":
    app.run(debug=True)
