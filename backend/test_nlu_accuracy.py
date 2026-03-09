import pickle
from sklearn.metrics import accuracy_score

# Load trained model
with open("nlp_model.pkl", "rb") as f:
    model = pickle.load(f)

# Test dataset (sentence, expected intent)
test_data = [
    ("I need motivation", "motivation"),
    ("Give me success advice", "success"),
    ("Tell me something funny", "funny"),
    ("I want a love quote", "love"),
    ("Give me life advice", "life"),
    ("How to stay motivated", "motivation"),
    ("Tell me a joke", "funny"),
    ("How to succeed in life", "success")
]

sentences = [x[0] for x in test_data]
true_labels = [x[1] for x in test_data]

# Predict intents
predicted_labels = model.predict(sentences)

# Calculate accuracy
accuracy = accuracy_score(true_labels, predicted_labels)

print("Predictions:")
for s, p in zip(sentences, predicted_labels):
    print(f"{s} -> {p}")

print("\nNLU Accuracy:", accuracy)