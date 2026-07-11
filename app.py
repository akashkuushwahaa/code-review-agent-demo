"""
UserLookup — a tiny internal service for looking up user records.
This is a deliberately minimal demo app used to test an automated
security review agent.
"""

import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)
DB_PATH = "users.db"


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


if __name__ == "__main__":
    init_db()
    app.run(debug=False, port=5000)
