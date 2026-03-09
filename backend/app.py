from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from database import get_random_quote
from nlp_classifier import get_intent, train_model

app = Flask(__name__)
CORS(app)

# Get backend directory
BASE_DIR = os.path.dirname(__file__)

# Check if transformer model exists
MODEL_DIR = os.path.join(BASE_DIR, "transformer_model")

# Train model automatically if it doesn't exist
if not os.path.exists(MODEL_DIR):
    print("Transformer model not found. Training model...")
    train_model()
else:
    print("Transformer model found. Loading model...")


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

    # Detect intent using transformer
    try:
        intent = get_intent(user_message)
    except Exception as e:
        print("Intent detection error:", e)
        intent = "unknown"

    print("Detected intent:", intent)

    # Greeting response
    if intent == "greet":
        return jsonify({
            "intent": "greet",
            "response": "Hello! Ask me for motivation, success, love, or funny quotes."
        })

    # Fetch quote from database
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
        "response": "Sorry, I couldn't find a quote for that. Try asking for motivation, success, love, or funny quotes."
    })


if __name__ == "__main__":
    app.run(debug=True)