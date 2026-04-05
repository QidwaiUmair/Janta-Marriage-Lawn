from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# ================= DATABASE CONNECTION =================
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Umair2020",
            database="lawn_booking"
        )
        return conn
    except Error as e:
        print(f"Database Error: {e}")
        return None

# ====================== MAIN ROUTES ======================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/rooms-hall')
def rooms_hall():
    return render_template('rooms-hall.html')

@app.route('/dj-music')
def dj_music():
    return render_template('dj-music.html')

@app.route('/parking')
def parking():
    return render_template('parking.html')

@app.route('/catering')
def catering():
    return render_template('catering.html')

@app.route('/lighting')
def lighting():
    return render_template('lighting.html')

# ================= ROOM BOOKING ROUTES =================

@app.route('/room-booking')
def room_booking():
    return render_template('room_booking.html')

@app.route('/room-book', methods=['POST'])
def room_book():
    try:
        data = request.get_json()

        name = data.get('name')
        phone = data.get('phone')
        check_in = data.get('check_in')
        check_out = data.get('check_out')
        room_type = data.get('room_type')

        if not all([name, phone, check_in, check_out]):
            return jsonify({"success": False, "message": "All fields are required!"}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({"success": False, "message": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO room_bookings (name, phone, check_in, check_out, room_type) VALUES (%s,%s,%s,%s,%s)",
            (name.strip(), phone.strip(), check_in, check_out, room_type)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True, "message": "Room booked successfully!"})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": "Server error"}), 500

# ================= EXISTING BOOKING =================

@app.route('/get-booked-dates')
def get_booked_dates():
    conn = get_db_connection()
    if not conn:
        return jsonify([]), 500
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT date FROM bookings WHERE date >= CURDATE()")
        dates = [str(row[0]) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return jsonify(dates)
    except Error as e:
        print(f"Error: {e}")
        return jsonify([]), 500

@app.route('/book', methods=['POST'])
def book():
    try:
        data = request.get_json()

        name = data.get('name')
        phone = data.get('phone')
        date = data.get('date')
        event = data.get('event')

        if not all([name, phone, date]):
            return jsonify({"success": False, "message": "Name, Phone aur Date zaroori hain!"}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({"success": False, "message": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO bookings (name, phone, date, event_type) VALUES (%s, %s, %s, %s)",
            (name.strip(), phone.strip(), date, event)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True, "message": "Booking request submitted successfully!"})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": "Server error occurred"}), 500

# ================= RUN =================

if __name__ == '__main__':
    app.run(debug=True)