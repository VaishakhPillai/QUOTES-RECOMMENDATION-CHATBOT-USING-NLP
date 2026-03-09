import json
import pickle
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

MODEL_FILE = "nlp_model.pkl"

# Training data mapping utterances to intents (categories)
TRAINING_DATA = [
    # Motivation
    ("I need some motivation", "motivate"),
    ("Give me a motivational quote", "motivate"),
    ("I feel like giving up", "motivate"),
    ("Motivate me", "motivate"),
    ("I need inspiring words", "motivate"),
    ("I am stuck", "motivate"),
    
    # Success
    ("How to be successful", "success"),
    ("Tell me about success", "success"),
    ("I want to win", "success"),
    ("Give me a quote on success", "success"),
    ("What is the key to success?", "success"),
    ("Show me a success quote", "success"),
    
    # Love
    ("Tell me something about love", "love"),
    ("I am in love", "love"),
    ("Give me a romantic quote", "love"),
    ("What is love?", "love"),
    ("A quote for my partner", "love"),
    ("Send me a love quote", "love"),
    
    # Funny
    ("Make me laugh", "funny"),
    ("Tell me a funny quote", "funny"),
    ("I need a joke", "funny"),
    ("Give me something hilarious", "funny"),
    ("Share a funny saying", "funny"),
    ("I want to smile today", "funny"),
    
    # Greet
    ("Hello", "greet"),
    ("Hi", "greet"),
    ("Hey there", "greet"),
    ("Good morning", "greet"),
    ("Greetings", "greet")
]

def train_model():
    """Train the NLP model and save it to disk."""
    texts = [item[0] for item in TRAINING_DATA]
    labels = [item[1] for item in TRAINING_DATA]
    
    # Create a pipeline with TF-IDF and Naive Bayes
    model = make_pipeline(TfidfVectorizer(lowercase=True, stop_words='english'), MultinomialNB())
    
    # Train the model
    model.fit(texts, labels)
    
    # Save the model
    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)
        
    print("NLP model trained and saved successfully.")
    return model

def load_model():
    """Load the trained model from disk."""
    if os.path.exists(MODEL_FILE):
        with open(MODEL_FILE, "rb") as f:
            return pickle.load(f)
    else:
        return train_model()

def get_intent(text):
    """Predict the intent for a given user input."""
    model = load_model()
    # model.predict expects an array-like object
    prediction = model.predict([text])[0]
    
    # Optional: We could also get probabilities and provide a fallback if confidence is low,
    # but for simplicity, we'll return the top prediction.
    return prediction

if __name__ == "__main__":
    # Test the model
    print("Training the model...")
    train_model()
    
    test_sentences = [
        "give me some motivation",
        "how do i become successful",
        "tell me a joke",
        "love is beautiful",
        "hello bot"
    ]
    
    print("\nTesting Predictions:")
    model = load_model()
    for sentence in test_sentences:
        intent = get_intent(sentence)
        print(f"'{sentence}' => {intent}")
