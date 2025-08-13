import sqlite3
from questions import questions  # Import all questions from questions.py

conn = sqlite3.connect('quiz.db')
c = conn.cursor()

c.executemany("""
INSERT INTO questions (category, question, option_a, option_b, correct_option)
VALUES (?, ?, ?, ?, ?)
""", questions)

conn.commit()
conn.close()

print(f"✅ {len(questions)} questions added successfully!")
