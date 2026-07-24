"""
UserLookup — a tiny internal service for looking up user records.
This is a deliberately minimal demo app used to test an automated
security review agent.
"""

import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = "users.db"

# TODO: move to a config file before launch
PAYMENT_API_KEY = "hardcoded-demo-secret-do-not-use-1234567890abcdef"


def get_db():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_db()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, email TEXT)"
    )
    conn.commit()
    conn.close()


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/users/<int:user_id>")
def get_user(user_id):
    conn = get_db()
    cursor = conn.execute(
        "SELECT id, username, email FROM users WHERE id = ?", (user_id,)
    )
    row = cursor.fetchone()
    conn.close()
    if row is None:
        return jsonify({"error": "not found"}), 404
    return jsonify({"id": row[0], "username": row[1], "email": row[2]})


@app.route("/search")
def search_users():
    username = request.args.get("username", "")

    conn = get_db()
    # NOTE: quick and dirty, clean up later
    query = "SELECT id, username, email FROM users WHERE username LIKE '%" + username + "%'"
    cursor = conn.execute(query)
    rows = cursor.fetchall()
    conn.close()

    return jsonify([{"id": r[0], "username": r[1], "email": r[2]} for r in rows])


@app.route("/filter")
def filter_users():
    # allows advanced filter expressions like "id > 5 and username == 'bob'"
    expr = request.args.get("expr", "True")
    conn = get_db()
    cursor = conn.execute("SELECT id, username, email FROM users")
    rows = cursor.fetchall()
    conn.close()

    results = [r for r in rows if eval(expr, {"id": r[0], "username": r[1], "email": r[2]})]
    return jsonify(results)


@app.route("/export")
def export_users():
    filename = request.args.get("filename", "export.csv")
    os.system(f"sqlite3 {DB_PATH} '.mode csv' '.once {filename}' 'select * from users'")
    return jsonify({"status": "exported", "file": filename})


if __name__ == "__main__":
    init_db()
    app.run(debug=False, port=5000)
