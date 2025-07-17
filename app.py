from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # Allow all origins for dev — restrict in prod

# Initialize database if not exists
def init_db():
    conn = sqlite3.connect("bookings.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            room TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return "Hotel Booking API running."

@app.route("/book", methods=["POST"])
def book():
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        room = data.get("room")

        if not all([name, email, room]):
            return jsonify({"status": "error", "message": "Missing fields"}), 400

        conn = sqlite3.connect("bookings.db")
        c = conn.cursor()
        c.execute("INSERT INTO bookings (name, email, room) VALUES (?, ?, ?)", (name, email, room))
        conn.commit()
        conn.close()

        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
