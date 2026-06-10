from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from groq import Groq

app = Flask(__name__)

# ==========================
# GROQ API KEY
# ==========================
client = Groq(
    api_key="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"
)

# ==========================
# UPLOAD FOLDER
# ==========================
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# ==========================
# DATABASE INIT
# ==========================
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ==========================
# HOME
# ==========================
@app.route("/")
def home():
    return render_template("index.html")

# ==========================
# ASK AI
# ==========================
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"answer": "No data received"})

        question = data.get("question")

        if not question:
            return jsonify({"answer": "Please enter a question"})

        print("Question:", question)

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ],
            model="llama-3.3-70b-versatile"
        )

        answer = response.choices[0].message.content

        print("Answer:", answer)

        # Save chat history
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO chat (question, answer) VALUES (?, ?)",
            (question, answer)
        )

        conn.commit()
        conn.close()

        return jsonify({"answer": answer})

    except Exception as e:
        print("ERROR:", e)

        return jsonify({
            "answer": f"Error: {str(e)}"
        })

# ==========================
# FILE UPLOAD
# ==========================
@app.route("/upload", methods=["POST"])
def upload():
    try:
        if "file" not in request.files:
            return "No file selected"

        file = request.files["file"]

        if file.filename == "":
            return "No file selected"

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)

        return "File Uploaded Successfully"

    except Exception as e:
        return f"Upload Error: {str(e)}"

# ==========================
# CHAT HISTORY
# ==========================
@app.route("/history")
def history():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT question, answer FROM chat ORDER BY id DESC"
    )

    data = cursor.fetchall()

    conn.close()

    return jsonify(data)

# ==========================
# RUN
# ==========================
if __name__ == "__main__":
    app.run(debug=True)