from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pickle

from database import get_random_quote

app = Flask(__name__)
CORS(app)

# Get backend directory
BASE_DIR = os.path.dirname(__file__)

# Load NLP model
model_path = os.path.join(BASE_DIR, "nlp_model.pkl")

try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    print("NLP model loaded successfully.")
except Exception as e:
    print("Error loading NLP model:", e)
    model = None


@app.route("/")
def home():
    return "QuoteBot API is running!"


@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({
            "response": "Invalid request"
        }), 400

    user_message = data["message"]

    # Default intent
    intent = "unknown"

    # Predict intent if model exists
    if model:
        try:
            intent = model.predict([user_message])[0]
        except Exception as e:
            print("Prediction error:", e)

    print("Detected intent:", intent)

    # Greeting intent
    if intent == "greet":
        return jsonify({
            "intent": "greet",
            "response": "Hello! Ask me for motivation, success, life, love, or funny quotes."
        })

    # Get quote from database
    quote = get_random_quote(intent)

    if quote:
        return jsonify({
            "intent": intent,
            "quote_details": {
                "quote_text": quote["quote_text"],
                "author": quote["author"]
            }
        })

    # Fallback response
    return jsonify({
        "intent": "unknown",
        "response": "Sorry, I couldn't find a quote for that. Try asking for motivation, success, life, love, or funny quotes."
    })


if __name__ == "__main__":
    app.run(debug=True)