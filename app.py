from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # <-- Add this
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)  # <-- Enable CORS

DB_FILE = 'database.db'

@app.route('/')
def home():
    return "Backend is running!"

@app.route('/book', methods=['POST'])
def book():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO bookings (name, email, phone, created_at)
                      VALUES (?, ?, ?, ?)''', (name, email, phone, date))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "Booking confirmed!"})

@app.route('/admin', methods=['GET'])
def admin_panel():
    auth = request.authorization
    if not auth or auth.username != 'user123' or auth.password != 'pass123':
        return jsonify({"message": "Unauthorized"}), 401

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bookings")
    rows = cursor.fetchall()
    conn.close()

    data = [
        {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "phone": row[3],
            "created_at": row[4]
        }
        for row in rows
    ]

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
