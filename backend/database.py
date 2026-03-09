import sqlite3
import os

# Get correct database path
BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "quotes.db")


def get_connection():
    """Create database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create table and seed quotes if empty."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            quote_text TEXT NOT NULL,
            author TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM quotes")
    count = cursor.fetchone()[0]

    if count == 0:
        print("Seeding database with quotes...")
        seed_data(cursor)
        conn.commit()
    else:
        print(f"Database already has {count} quotes.")

    conn.close()


def seed_data(cursor):
    """Insert default quotes."""

    quotes = [

        # Motivation
        ("motivation", "Believe you can and you're halfway there.", "Theodore Roosevelt"),
        ("motivation", "The only way to do great work is to love what you do.", "Steve Jobs"),
        ("motivation", "Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
        ("motivation", "Act as if what you do makes a difference. It does.", "William James"),
        ("motivation", "The future depends on what you do today.", "Mahatma Gandhi"),

        # Success
        ("success", "Success usually comes to those who are too busy to be looking for it.", "Henry David Thoreau"),
        ("success", "Success is not final, failure is not fatal.", "Winston Churchill"),
        ("success", "The way to get started is to quit talking and begin doing.", "Walt Disney"),
        ("success", "Opportunities don't happen. You create them.", "Chris Grosser"),

        # Life
        ("life", "Life is what happens when you're busy making other plans.", "John Lennon"),
        ("life", "Turn your wounds into wisdom.", "Oprah Winfrey"),
        ("life", "The purpose of our lives is to be happy.", "Dalai Lama"),

        # Love
        ("love", "Where there is love there is life.", "Mahatma Gandhi"),
        ("love", "Love is composed of a single soul inhabiting two bodies.", "Aristotle"),
        ("love", "Being deeply loved by someone gives you strength.", "Lao Tzu"),

        # Funny
        ("funny", "People say nothing is impossible, but I do nothing every day.", "A. A. Milne"),
        ("funny", "I'm not lazy, I'm just on energy-saving mode.", "Unknown"),
        ("funny", "I always wanted to be somebody, but now I realize I should have been more specific.", "Lily Tomlin")
    ]

    cursor.executemany("""
        INSERT INTO quotes (category, quote_text, author)
        VALUES (?, ?, ?)
    """, quotes)

    print(f"{len(quotes)} quotes inserted successfully.")


def map_intent_to_category(intent):
    """Map ML intent to database category."""

    intent_map = {
        "motivate": "motivation",
        "success": "success",
        "love": "love",
        "funny": "funny",
        "life": "life"
    }

    return intent_map.get(intent, intent)


def get_random_quote(category=None):
    """Get a random quote by category."""

    conn = get_connection()
    cursor = conn.cursor()

    if category:
        category = map_intent_to_category(category)

        cursor.execute(
            "SELECT category, quote_text, author FROM quotes WHERE category=? ORDER BY RANDOM() LIMIT 1",
            (category,)
        )
    else:
        cursor.execute(
            "SELECT category, quote_text, author FROM quotes ORDER BY RANDOM() LIMIT 1"
        )

    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)

    return None


if __name__ == "__main__":

    init_db()

    print("\nTesting database:\n")

    print("Random Quote:")
    print(get_random_quote())

    print("\nMotivation Quote:")
    print(get_random_quote("motivate"))