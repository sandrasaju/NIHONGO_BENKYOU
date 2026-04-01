from flask import Flask, render_template, request, session, jsonify, redirect, url_for, flash
import json, random, os
from functools import wraps

# Load .env manually
_env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_env_file):
    with open(_env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip()  # override, not setdefault

from database import init_db
from auth import (generate_otp, send_otp_email, store_otp, verify_otp,
                  register_user, verify_user, login_user,
                  add_reward_points, get_all_users)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-me-in-production")

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with app.app_context():
    init_db()

# ── Helpers ────────────────────────────────────────────────────

def load_vocab(level=None):
    with open(os.path.join(BASE_DIR, "vocab.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    if level:
        data = [w for w in data if w["level"] == level]
    return data

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated

# ── User Auth Routes ───────────────────────────────────────────

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "").strip()
        if not identifier or not password:
            flash("All fields are required.", "error")
            return render_template("register.html")

        ok, status = register_user(identifier, password)

        if not ok:
            if status == "already_verified":
                flash("This email/phone is already registered and verified. Please log in.", "error")
            else:
                flash(status, "error")
            return render_template("register.html")

        otp = generate_otp()
        store_otp(identifier, otp)
        sent = send_otp_email(identifier, otp)
        session["pending_identifier"] = identifier

        if not sent:
            session["dev_otp"] = otp
            flash("Dev mode: your OTP is shown on the next page.", "info")
        else:
            flash("OTP sent! Check your email.", "info")

        return redirect(url_for("verify_otp_page"))
    return render_template("register.html")

@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp_page():
    identifier = session.get("pending_identifier")
    if not identifier:
        return redirect(url_for("register"))
    if request.method == "POST":
        otp = request.form.get("otp", "").strip()
        if verify_otp(identifier, otp):
            verify_user(identifier)
            session.pop("pending_identifier", None)
            session.pop("dev_otp", None)
            flash("Account verified! You can now log in.", "success")
            return redirect(url_for("login"))
        flash("Invalid or expired OTP. Try again.", "error")
    dev_otp = session.get("dev_otp")
    return render_template("verify_otp.html", identifier=identifier, dev_otp=dev_otp)

@app.route("/resend-otp")
def resend_otp():
    identifier = session.get("pending_identifier")
    if not identifier:
        return redirect(url_for("register"))
    otp = generate_otp()
    store_otp(identifier, otp)
    send_otp_email(identifier, otp)
    session["dev_otp"] = otp
    flash("A new OTP has been generated.", "info")
    return redirect(url_for("verify_otp_page"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("index"))
    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "").strip()
        user, err = login_user(identifier, password)
        if err:
            flash(err, "error")
            return render_template("login.html")
        session["user_id"] = user["id"]
        session["user_identifier"] = user["identifier"]
        session["reward_points"] = user["reward_points"]
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return render_template("logout.html")

# ── Public Routes ──────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/quiz")
@login_required
def quiz():
    level = request.args.get("level", "N5")
    session["level"] = level
    session["score"] = 0
    session["question_index"] = 0
    vocab = load_vocab(level)
    session["questions"] = random.sample(vocab, min(10, len(vocab)))
    return render_template("quiz.html", level=level)

@app.route("/api/question")
@login_required
def get_question():
    questions = session.get("questions", [])
    idx = session.get("question_index", 0)
    if idx >= len(questions):
        return jsonify({"done": True, "score": session.get("score", 0), "total": len(questions)})
    q = questions[idx]
    all_vocab = load_vocab(session.get("level", "N5"))
    wrong_options = [w["meaning"] for w in all_vocab if w["meaning"] != q["meaning"]]
    options = random.sample(wrong_options, min(3, len(wrong_options))) + [q["meaning"]]
    random.shuffle(options)
    return jsonify({
        "done": False,
        "word": q["word"],
        "reading": q["reading"],
        "options": options,
        "current": idx + 1,
        "total": len(questions)
    })

@app.route("/api/answer", methods=["POST"])
@login_required
def check_answer():
    data = request.get_json()
    questions = session.get("questions", [])
    idx = session.get("question_index", 0)
    if idx >= len(questions):
        return jsonify({"error": "No more questions"}), 400
    correct = questions[idx]["meaning"]
    is_correct = data.get("answer") == correct
    if is_correct:
        session["score"] = session.get("score", 0) + 1
    session["question_index"] = idx + 1
    return jsonify({"correct": is_correct, "correct_answer": correct})

@app.route("/result")
@login_required
def result():
    score = session.get("score", 0)
    total = len(session.get("questions", []))
    level = session.get("level", "N5")
    perfect = score == total == 10
    if perfect:
        add_reward_points(session["user_id"], 10)
        session["reward_points"] = session.get("reward_points", 0) + 10
    return render_template("result.html", score=score, total=total, level=level, perfect=perfect,
                           reward_points=session.get("reward_points", 0))

# ── Admin Routes ───────────────────────────────────────────────

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        if (request.form.get("username") == ADMIN_USERNAME and
                request.form.get("password") == ADMIN_PASSWORD):
            session["admin_logged_in"] = True
            return redirect(url_for("wordlist"))
        error = "Invalid credentials"
    return render_template("admin_login.html", error=error)

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("index"))

@app.route("/admin/users")
@admin_required
def admin_users():
    users = get_all_users()
    return render_template("admin_users.html", users=users)

@app.route("/wordlist")
@admin_required
def wordlist():
    level = request.args.get("level", "N5")
    vocab = load_vocab(level)
    return render_template("wordlist.html", vocab=vocab, level=level)

if __name__ == "__main__":
    debug = os.environ.get("FLASK_ENV") != "production"
    app.run(debug=debug)
