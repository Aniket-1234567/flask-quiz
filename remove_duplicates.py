# remove_duplicates.py
import sqlite3

DB_NAME = "quiz.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Delete duplicates: keep the row with the smallest id for each unique question
cursor.execute('''
DELETE FROM questions
WHERE id NOT IN (
    SELECT MIN(id)
    FROM questions
    GROUP BY question
)
''')

conn.commit()
conn.close()

print("✅ Duplicate questions removed!")
