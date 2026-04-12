import random, smtplib, os
from email.mime.text import MIMEText
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db, DB_TYPE

PH = "%s" if DB_TYPE == "mysql" else "?"

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
        msg = MIMEText(f"Your JLPT Trainer OTP: {otp}\n\nExpires in 10 minutes.")
        msg["Subject"] = "Your JLPT Trainer OTP"
        msg["From"] = smtp_user
        msg["To"] = to_email
        with smtplib.SMTP(smtp_host, smtp_port) as s:
            s.starttls(); s.login(smtp_user, smtp_pass); s.send_message(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def _row(cursor, row):
    """Normalize row to dict for both MySQL and SQLite."""
    if row is None:
        return None
    if isinstance(row, dict):
        return row
    return dict(row)

def store_otp(identifier, otp):
    conn = get_db()
    if DB_TYPE == "mysql":
        c = conn.cursor()
        c.execute(f"DELETE FROM otp_store WHERE identifier = {PH}", (identifier,))
        c.execute(f"INSERT INTO otp_store (identifier, otp) VALUES ({PH},{PH})", (identifier, otp))
        conn.commit(); c.close()
    else:
        conn.execute(f"DELETE FROM otp_store WHERE identifier = {PH}", (identifier,))
        conn.execute(f"INSERT INTO otp_store (identifier, otp) VALUES ({PH},{PH})", (identifier, otp))
        conn.commit()
    conn.close()

def verify_otp(identifier, otp):
    conn = get_db()
    if DB_TYPE == "mysql":
        c = conn.cursor(dictionary=True)
        c.execute(f"SELECT otp FROM otp_store WHERE identifier = {PH} ORDER BY created_at DESC LIMIT 1", (identifier,))
        row = c.fetchone(); c.close()
    else:
        row = conn.execute(f"SELECT otp FROM otp_store WHERE identifier = {PH} ORDER BY created_at DESC LIMIT 1", (identifier,)).fetchone()
    conn.close()
    return row and (row["otp"] if isinstance(row, dict) else row[0]) == otp

def register_user(identifier, password):
    conn = get_db()
    id_type = "email" if is_email(identifier) else "phone"
    pw_hash = generate_password_hash(password)
    if DB_TYPE == "mysql":
        c = conn.cursor(dictionary=True)
        c.execute(f"SELECT * FROM users WHERE identifier = {PH}", (identifier,))
        existing = c.fetchone()
    else:
        existing = _row(None, conn.execute(f"SELECT * FROM users WHERE identifier = {PH}", (identifier,)).fetchone())
    if existing:
        if existing and existing.get("is_verified") if isinstance(existing, dict) else (existing["is_verified"] if existing else False):
            conn.close(); return False, "already_verified"
        if DB_TYPE == "mysql":
            c.execute(f"UPDATE users SET password_hash = {PH} WHERE identifier = {PH}", (pw_hash, identifier))
            conn.commit(); c.close()
        else:
            conn.execute(f"UPDATE users SET password_hash = {PH} WHERE identifier = {PH}", (pw_hash, identifier))
            conn.commit()
        conn.close(); return True, "resend"
    try:
        if DB_TYPE == "mysql":
            c.execute(f"INSERT INTO users (identifier, password_hash, identifier_type) VALUES ({PH},{PH},{PH})", (identifier, pw_hash, id_type))
            conn.commit(); c.close()
        else:
            conn.execute(f"INSERT INTO users (identifier, password_hash, identifier_type) VALUES ({PH},{PH},{PH})", (identifier, pw_hash, id_type))
            conn.commit()
        return True, None
    except Exception:
        return False, "Something went wrong."
    finally:
        conn.close()

def verify_user(identifier):
    conn = get_db()
    if DB_TYPE == "mysql":
        c = conn.cursor(); c.execute(f"UPDATE users SET is_verified = 1 WHERE identifier = {PH}", (identifier,)); conn.commit(); c.close()
    else:
        conn.execute(f"UPDATE users SET is_verified = 1 WHERE identifier = {PH}", (identifier,)); conn.commit()
    conn.close()

def login_user(identifier, password):
    conn = get_db()
    if DB_TYPE == "mysql":
        c = conn.cursor(dictionary=True)
        c.execute(f"SELECT * FROM users WHERE identifier = {PH}", (identifier,))
        user = c.fetchone(); c.close()
    else:
        row = conn.execute(f"SELECT * FROM users WHERE identifier = {PH}", (identifier,)).fetchone()
        user = dict(row) if row else None
    conn.close()
    if not user: return None, "No account found with that email/phone."
    if not user["is_verified"]: return None, "Please verify your account first."
    if not check_password_hash(user["password_hash"], password): return None, "Incorrect password."
    return user, None

def add_reward_points(user_id, points):
    conn = get_db()
    if DB_TYPE == "mysql":
        c = conn.cursor(); c.execute(f"UPDATE users SET reward_points = reward_points + {PH} WHERE id = {PH}", (points, user_id)); conn.commit(); c.close()
    else:
        conn.execute(f"UPDATE users SET reward_points = reward_points + {PH} WHERE id = {PH}", (points, user_id)); conn.commit()
    conn.close()

def get_all_users():
    conn = get_db()
    if DB_TYPE == "mysql":
        c = conn.cursor(dictionary=True)
        c.execute("SELECT id, identifier, identifier_type, reward_points, is_verified, created_at FROM users ORDER BY created_at DESC")
        users = c.fetchall(); c.close()
    else:
        users = [dict(r) for r in conn.execute("SELECT id, identifier, identifier_type, reward_points, is_verified, created_at FROM users ORDER BY created_at DESC").fetchall()]
    conn.close()
    return users
