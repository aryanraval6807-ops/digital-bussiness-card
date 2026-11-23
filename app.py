"""Digital Business Card - Flask + SQLite backend."""
import os
import sqlite3
from flask import Flask, render_template, request, jsonify, g

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "card.db")

app = Flask(__name__)

DEFAULT_CARD = {
    "name": "Dhairya Darji",
    "designation": "Web Developer",
    "company": "CodeNest Studio",
    "phone": "9876543210",
    "email": "dhairya@codenest.dev",
    "email2": "dhairya.darji@example.com",
    "address": "Vadodara, Gujarat",
    "linkedin": "linkedin.com/in/dhairyadarji",
}
FIELDS = list(DEFAULT_CARD.keys())


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.execute(
        """CREATE TABLE IF NOT EXISTS card (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            name TEXT NOT NULL, designation TEXT, company TEXT,
            phone TEXT, email TEXT, email2 TEXT, address TEXT, linkedin TEXT
        )"""
    )
    if db.execute("SELECT COUNT(*) FROM card").fetchone()[0] == 0:
        cols = ", ".join(FIELDS)
        marks = ", ".join("?" for _ in FIELDS)
        db.execute(
            f"INSERT INTO card (id, {cols}) VALUES (1, {marks})",
            [DEFAULT_CARD[f] for f in FIELDS],
        )
    db.commit()
    db.close()


def read_card():
    row = get_db().execute("SELECT * FROM card WHERE id = 1").fetchone()
    return {f: row[f] or "" for f in FIELDS}


@app.route("/")
def index():
    return render_template("index.html", card=read_card())


@app.route("/api/card", methods=["GET"])
def api_get_card():
    return jsonify(read_card())


@app.route("/api/card", methods=["POST"])
def api_save_card():
    data = request.get_json(silent=True) or {}
    clean = {f: str(data.get(f, "")).strip()[:120] for f in FIELDS}
    if not clean["name"]:
        return jsonify({"ok": False, "error": "Name is required"}), 400
    sets = ", ".join(f"{f} = ?" for f in FIELDS)
    db = get_db()
    db.execute(f"UPDATE card SET {sets} WHERE id = 1", [clean[f] for f in FIELDS])
    db.commit()
    return jsonify({"ok": True, "card": clean})


@app.route("/api/card/reset", methods=["POST"])
def api_reset():
    sets = ", ".join(f"{f} = ?" for f in FIELDS)
    db = get_db()
    db.execute(f"UPDATE card SET {sets} WHERE id = 1", [DEFAULT_CARD[f] for f in FIELDS])
    db.commit()
    return jsonify({"ok": True, "card": DEFAULT_CARD})


init_db()

if __name__ == "__main__":
    app.run(debug=True)
