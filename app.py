from flask import Flask, render_template, request, jsonify
import sqlite3, random

app = Flask(__name__)

# ---------- Database Setup ----------
def init_db():
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    question TEXT NOT NULL,
                    option_a TEXT NOT NULL,
                    option_b TEXT NOT NULL,
                    correct_option TEXT NOT NULL
                )''')
    conn.commit()

    # Insert sample data if empty
    c.execute("SELECT COUNT(*) FROM questions")
    if c.fetchone()[0] == 0:
        sample_questions = [
            ("heart", "How many chambers does the human heart have?", "2", "4", "4"),
            ("heart", "Which side of the heart pumps blood to the lungs?", "Right", "Left", "Right"),
            ("lungs", "How many lungs does a human have?", "1", "2", "2"),
            ("lungs", "Which gas do lungs absorb from the air?", "Oxygen", "Carbon Dioxide", "Oxygen"),
            ("dental", "How many permanent teeth does an adult human have?", "32", "28", "32"),
            ("dental", "Which type of teeth are used for cutting food?", "Incisors", "Molars", "Incisors"),
            ("brain", "Which part of the brain controls balance?", "Cerebellum", "Medulla", "Cerebellum"),
            ("brain", "What is the average weight of the human brain?", "1.4 kg", "800 g", "1.4 kg"),
            ("heart", "What is the normal resting heart rate range?", "60-100 bpm", "120-160 bpm", "60-100 bpm"),
            ("lungs", "What protects the lungs?", "Rib cage", "Skull", "Rib cage"),
        ]
        c.executemany("INSERT INTO questions (category, question, option_a, option_b, correct_option) VALUES (?, ?, ?, ?, ?)", sample_questions)
        conn.commit()
    conn.close()



init_db()

# ---------- Routes ----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/category/<cat>')
def category(cat):
    return render_template('category.html', category=cat)

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')
@app.route('/get_question/<cat>')
def get_question(cat):
    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questions WHERE category=?", (cat,))
    all_qs = c.fetchall()
    conn.close()
    if all_qs:
        q = random.choice(all_qs)
        return jsonify({
            "id": q[0],
            "question": q[2],
            "option_a": q[3],
            "option_b": q[4]
        })
    return jsonify({})

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    q_id = data.get('id')
    answer = data.get('answer')

    conn = sqlite3.connect('quiz.db')
    c = conn.cursor()
    c.execute("SELECT correct_option FROM questions WHERE id=?", (q_id,))
    correct = c.fetchone()[0]
    conn.close()

    return jsonify({"correct": answer == correct, "correct_option": correct})

if __name__ == '__main__':
    app.run(debug=True)
