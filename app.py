import os
import re
from datetime import datetime
from functools import wraps

import mysql.connector
from mysql.connector import Error
from flask import Flask, jsonify, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-development-secret-key")

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "port": int(os.environ.get("DB_PORT", "3306")),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "easydonate_db"),
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def json_error(message, status=400):
    return jsonify({"error": message}), status

@app.route("/")
def home():
    return render_template("index.html")

@app.get("/api/health")
def health():
    try:
        conn = get_connection()
        conn.close()
        return jsonify({"status": "ok", "database": "connected"})
    except Error:
        return json_error("Flask is running, but MySQL connection failed. Check database settings.", 503)

@app.post("/api/register")
def register():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return json_error("Enter a valid email address.")
    if len(password) < 8:
        return json_error("Password must contain at least 8 characters.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (email, password_hash) VALUES (%s, %s)",
                    (email, generate_password_hash(password)))
        conn.commit()
        user_id = cur.lastrowid
        session["user_id"] = user_id
        session["email"] = email
        cur.close()
        conn.close()
        return jsonify({"message": "Account created successfully.", "user": {"id": user_id, "email": email}}), 201
    except mysql.connector.IntegrityError:
        return json_error("An account with this email already exists.", 409)
    except Error:
        return json_error("Database error. Check that MySQL is running and schema.sql was imported.", 503)

@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, email, password_hash FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if not user or not check_password_hash(user["password_hash"], password):
            return json_error("Invalid email or password.", 401)
        session["user_id"] = user["id"]
        session["email"] = user["email"]
        return jsonify({"message": "Login successful.", "user": {"id": user["id"], "email": user["email"]}})
    except Error:
        return json_error("Database error. Check that MySQL is running and schema.sql was imported.", 503)

@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logged out."})

@app.post("/api/donations")
def create_donation():
    data = request.get_json(silent=True) or {}
    required = ["donor_name", "category", "description", "quantity", "pickup_date", "pickup_time", "address"]
    if any(not str(data.get(key, "")).strip() for key in required):
        return json_error("Please complete every donation field.")
    try:
        quantity = int(data["quantity"])
        if quantity < 1:
            return json_error("Quantity must be at least 1.")
        pickup_date = datetime.strptime(data["pickup_date"], "%Y-%m-%d").date()
        pickup_time = datetime.strptime(data["pickup_time"], "%H:%M").time()
    except (ValueError, TypeError):
        return json_error("Enter a valid quantity, pickup date and pickup time.")
    allowed = {"Clothes", "Books", "Furniture", "Electronics", "Food", "Other"}
    category = str(data["category"]).strip()
    if category not in allowed:
        return json_error("Select a valid donation category.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""INSERT INTO donations
            (user_id, donor_name, category, description, quantity, pickup_date, pickup_time, address, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'Submitted')""",
            (session.get("user_id"), str(data["donor_name"]).strip(), category,
             str(data["description"]).strip(), quantity, pickup_date, pickup_time,
             str(data["address"]).strip()))
        conn.commit()
        donation_id = cur.lastrowid
        cur.close()
        conn.close()
        return jsonify({"message": "Donation saved successfully.", "id": donation_id, "status": "Submitted"}), 201
    except Error:
        return json_error("Could not save donation. Check MySQL connection and schema.sql.", 503)

@app.get("/api/donations")
def list_donations():
    # Only return the current signed-in user's donations.
    if not session.get("user_id"):
        return json_error("Please log in to view your saved donations.", 401)
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("""SELECT id, donor_name, category, description, quantity,
                       pickup_date, pickup_time, status, created_at
                       FROM donations WHERE user_id=%s ORDER BY id DESC""", (session["user_id"],))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        for row in rows:
            row["pickup_date"] = str(row["pickup_date"])
            row["pickup_time"] = str(row["pickup_time"])
            row["created_at"] = str(row["created_at"])
        return jsonify({"donations": rows})
    except Error:
        return json_error("Could not retrieve donations from MySQL.", 503)

@app.post("/api/messages")
def save_message():
    data = request.get_json(silent=True) or {}
    name, email, message = (str(data.get(k, "")).strip() for k in ("name", "email", "message"))
    if not name or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) or not message:
        return json_error("Enter your name, a valid email and a message.")
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO contact_messages (name, email, message) VALUES (%s,%s,%s)",
                    (name, email, message))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Thank you! Your message has been saved."}), 201
    except Error:
        return json_error("Could not save message. Check MySQL connection and schema.sql.", 503)

if __name__ == "__main__":
    app.run(debug=True)
