
from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Create DB if not exists
def init_db():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT,
            room TEXT,
            date TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# POST API for form submission
@app.route('/book', methods=['POST'])
def book_room():
    name = request.form['name']
    contact = request.form['contact']
    room = request.form['room']
    date = request.form['date']

    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute('INSERT INTO bookings (name, contact, room, date) VALUES (?, ?, ?, ?)',
              (name, contact, room, date))
    conn.commit()
    conn.close()

    return "<h2>✅ Booking received! We'll contact you shortly.</h2>"

@app.route('/admin')
def admin():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute('SELECT * FROM bookings')
    rows = c.fetchall()
    conn.close()
    return render_template('admin.html', bookings=rows)


if __name__ == '__main__':
    app.run(debug=True)
