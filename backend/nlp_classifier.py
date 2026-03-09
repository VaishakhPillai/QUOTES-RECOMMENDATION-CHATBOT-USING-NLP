import os
import torch
import numpy as np
from datasets import Dataset
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments
)

MODEL_DIR = "transformer_model"

# Training dataset
TRAINING_DATA = [

    # Motivation
    ("I need motivation", "motivate"),
    ("Motivate me", "motivate"),
    ("Give me inspiration", "motivate"),
    ("Encourage me", "motivate"),
    ("I feel like giving up", "motivate"),
    ("Push me to work harder", "motivate"),
    ("Tell me something inspiring", "motivate"),
    ("Help me stay positive", "motivate"),
    ("Give me motivational words", "motivate"),
    ("Inspire me today", "motivate"),

    # Success
    ("How can I become successful", "success"),
    ("Tell me about success", "success"),
    ("Give me a success quote", "success"),
    ("How to win in life", "success"),
    ("Teach me success mindset", "success"),
    ("Success advice please", "success"),
    ("Guide me to success", "success"),
    ("How do people succeed", "success"),
    ("Give me achievement advice", "success"),
    ("Tell me a success message", "success"),

    # Love
    ("Tell me something about love", "love"),
    ("Give me a love quote", "love"),
    ("Romantic quote please", "love"),
    ("I am in love", "love"),
    ("Share a romantic message", "love"),
    ("Love advice please", "love"),
    ("Tell me a romantic thought", "love"),
    ("Love is beautiful", "love"),
    ("Send me a love quote", "love"),
    ("Relationship advice", "love"),

    # Funny
    ("Tell me a joke", "funny"),
    ("Make me laugh", "funny"),
    ("Say something funny", "funny"),
    ("Share something hilarious", "funny"),
    ("Give me a funny quote", "funny"),
    ("Tell me something silly", "funny"),
    ("I want a joke", "funny"),
    ("Make my day funny", "funny"),
    ("Say a humorous quote", "funny"),
    ("Funny line please", "funny"),

    # Greeting
    ("Hello", "greet"),
    ("Hi", "greet"),
    ("Hey there", "greet"),
    ("Good morning", "greet"),
    ("Greetings", "greet"),
    ("Hello bot", "greet"),
    ("Hi assistant", "greet"),
    ("Nice to meet you", "greet"),
    ("Hey chatbot", "greet"),
    ("Hello friend", "greet")
]

# Label mapping
LABELS = list(set(label for _, label in TRAINING_DATA))
label2id = {label: i for i, label in enumerate(LABELS)}
id2label = {i: label for label, i in label2id.items()}


def prepare_dataset(texts, labels):

    tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")

    dataset = Dataset.from_dict({
        "text": texts,
        "label": labels
    })

    def tokenize(example):
        return tokenizer(
            example["text"],
            padding="max_length",
            truncation=True,
            max_length=32
        )

    dataset = dataset.map(tokenize)

    return dataset, tokenizer


def train_model():

    texts = [t[0] for t in TRAINING_DATA]
    labels = [label2id[t[1]] for t in TRAINING_DATA]

    dataset, tokenizer = prepare_dataset(texts, labels)

    model = DistilBertForSequenceClassification.from_pretrained(
        "distilbert-base-uncased",
        num_labels=len(LABELS)
    )

    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=25,
        per_device_train_batch_size=4,
        logging_steps=10,
        save_strategy="no",
        seed=42
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset
    )

    trainer.train()

    os.makedirs(MODEL_DIR, exist_ok=True)

    model.save_pretrained(MODEL_DIR)
    tokenizer.save_pretrained(MODEL_DIR)

    print("Transformer model trained and saved.")


def load_model():

    tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_DIR)
    model = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR)

    return tokenizer, model


def get_intent(text):

    tokenizer, model = load_model()

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    outputs = model(**inputs)

    probs = torch.nn.functional.softmax(outputs.logits, dim=1)

    predicted = torch.argmax(probs).item()

    return id2label[predicted]


if __name__ == "__main__":

    if not os.path.exists(MODEL_DIR):
        print("Training Transformer model...")
        train_model()
    else:
        print("Model already trained.")

    print("\nTesting model predictions:\n")

    test_sentences = [
        "give me motivation",
        "tell me a joke",
        "how can i succeed",
        "i love someone",
        "hello"
    ]

    for sentence in test_sentences:
        print(sentence, "->", get_intent(sentence))