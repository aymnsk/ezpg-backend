from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)

# === DATABASE SETUP ===
def init_db():
    with sqlite3.connect("bookings.db") as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            room TEXT NOT NULL,
            date TEXT NOT NULL
        )
        """)
        conn.commit()

init_db()

@app.route('/')
def home():
    return "<h2>🎯 EzPG Backend Live</h2><p>POST to <code>/book</code> or view <code>/admin</code></p>"

# === BOOKING API ===
@app.route('/book', methods=['POST'])
def book():
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    room = data.get("room")
    date = data.get("date")

    with sqlite3.connect("bookings.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO bookings (name, email, phone, room, date) VALUES (?, ?, ?, ?, ?)",
                  (name, email, phone, room, date))
        conn.commit()

    return jsonify({"message": "Booking successful"}), 200

# === ADMIN PANEL ===
@app.route('/admin', methods=['GET'])
def admin():
    with sqlite3.connect("bookings.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM bookings ORDER BY id DESC")
        bookings = c.fetchall()
    return render_template("admin.html", bookings=bookings)
