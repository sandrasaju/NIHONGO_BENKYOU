import random, smtplib, os
from email.mime.text import MIMEText
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db

def is_email(identifier):
    return "@" in identifier

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(to_email, otp):
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_pass = os.environ.get("SMTP_PASS", "")
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))

    if not smtp_user or not smtp_pass:
        print(f"\n[DEV MODE] OTP for {to_email}: {otp}\n")
        return False
    try:
        msg = MIMEText(f"""
🎌 JLPT AI Trainer — Your OTP

Your verification code is: {otp}

This code expires in 10 minutes.
        """)
        msg["Subject"] = "Your JLPT Trainer OTP"
        msg["From"] = smtp_user
        msg["To"] = to_email
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def store_otp(identifier, otp):
    db = get_db()
    db.execute("DELETE FROM otp_store WHERE identifier = ?", (identifier,))
    db.execute("INSERT INTO otp_store (identifier, otp) VALUES (?, ?)", (identifier, otp))
    db.commit()
    db.close()

def verify_otp(identifier, otp):
    db = get_db()
    row = db.execute(
        "SELECT otp FROM otp_store WHERE identifier = ? ORDER BY created_at DESC LIMIT 1",
        (identifier,)
    ).fetchone()
    db.close()
    return row and row["otp"] == otp

def register_user(identifier, password):
    db = get_db()
    id_type = "email" if is_email(identifier) else "phone"
    pw_hash = generate_password_hash(password)

    # Check if already exists
    existing = db.execute("SELECT * FROM users WHERE identifier = ?", (identifier,)).fetchone()
    if existing:
        if existing["is_verified"]:
            db.close()
            return False, "already_verified"
        else:
            # Unverified — update password and resend OTP
            db.execute("UPDATE users SET password_hash = ? WHERE identifier = ?", (pw_hash, identifier))
            db.commit()
            db.close()
            return True, "resend"

    try:
        db.execute(
            "INSERT INTO users (identifier, password_hash, identifier_type) VALUES (?, ?, ?)",
            (identifier, pw_hash, id_type)
        )
        db.commit()
        return True, None
    except Exception:
        return False, "Something went wrong. Please try again."
    finally:
        db.close()

def verify_user(identifier):
    db = get_db()
    db.execute("UPDATE users SET is_verified = 1 WHERE identifier = ?", (identifier,))
    db.commit()
    db.close()

def login_user(identifier, password):
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE identifier = ?", (identifier,)
    ).fetchone()
    db.close()
    if not user:
        return None, "No account found with that email/phone."
    if not user["is_verified"]:
        return None, "Please verify your account first."
    if not check_password_hash(user["password_hash"], password):
        return None, "Incorrect password."
    return dict(user), None

def add_reward_points(user_id, points):
    db = get_db()
    db.execute("UPDATE users SET reward_points = reward_points + ? WHERE id = ?", (points, user_id))
    db.commit()
    db.close()

def get_all_users():
    db = get_db()
    users = db.execute(
        "SELECT id, identifier, identifier_type, reward_points, is_verified, created_at FROM users ORDER BY created_at DESC"
    ).fetchall()
    db.close()
    return [dict(u) for u in users]
