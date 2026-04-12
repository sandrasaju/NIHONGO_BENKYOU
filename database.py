import os

def _get_db_type():
    # Read .env manually if not already loaded
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())
    return os.environ.get("DB_TYPE", "sqlite")

DB_TYPE = _get_db_type()

# ── MySQL ──────────────────────────────────────────────────────
def get_mysql():
    import mysql.connector
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", ""),
        database=os.environ.get("DB_NAME", "jlpt_trainer")
    )

# ── SQLite ─────────────────────────────────────────────────────
def get_sqlite():
    import sqlite3
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(os.path.join(BASE_DIR, "users.db"))
    conn.row_factory = sqlite3.Row
    return conn

def get_db():
    if DB_TYPE == "mysql":
        return get_mysql()
    return get_sqlite()

def init_db():
    if DB_TYPE == "mysql":
        conn = get_mysql()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                identifier VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                identifier_type VARCHAR(10) NOT NULL,
                reward_points INT DEFAULT 0,
                is_verified TINYINT(1) DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS otp_store (
                id INT AUTO_INCREMENT PRIMARY KEY,
                identifier VARCHAR(255) NOT NULL,
                otp VARCHAR(10) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
    else:
        conn = get_sqlite()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                identifier TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                identifier_type TEXT NOT NULL,
                reward_points INTEGER DEFAULT 0,
                is_verified INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS otp_store (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                identifier TEXT NOT NULL,
                otp TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        conn.close()
