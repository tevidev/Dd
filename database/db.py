import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from threading import Lock

DB_LOCK = Lock()
# =========================================================
# CONFIG
# =========================================================
# Railway inyecta AUTOMÁTICAMENTE estas variables
# Usamos DATABASE_URL y como respaldo DATABASE_PUBLIC_URL

DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("DATABASE_PUBLIC_URL")

if not DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL no está configurada en Railway")

# =========================================================
# CONEXIÓN
# =========================================================

def get_db():
    return psycopg2.connect(
        DATABASE_URL,
        cursor_factory=RealDictCursor,
        sslmode="require"
    )

# =========================================================
# INIT DB (SE EJECUTA AL ARRANCAR)
# =========================================================

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # ---- USERS ----
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id BIGINT PRIMARY KEY,
        username TEXT,
        rank TEXT DEFAULT 'USER',
        credits INTEGER DEFAULT 0,
        expires_at TIMESTAMP
    );
    """)

    # ---- KEYS ----
    cur.execute("""
    CREATE TABLE IF NOT EXISTS keys (
        key TEXT PRIMARY KEY,
        days INTEGER DEFAULT 0,
        credits INTEGER DEFAULT 0,
        used BOOLEAN DEFAULT FALSE
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

# =========================================================
# USUARIOS
# =========================================================

def register_user(user_id, username):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO users (user_id, username)
    VALUES (%s, %s)
    ON CONFLICT (user_id) DO NOTHING
    """, (user_id, username))

    conn.commit()
    cur.close()
    conn.close()

def get_user(user_id: int):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT user_id, username, rank, credits, expires_at
    FROM users
    WHERE user_id=%s
    """, (user_id,))

    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def get_rank(user_id: int):
    user = get_user(user_id)
    return user["rank"] if user else None

def set_rank(user_id: int, rank: str):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    UPDATE users
    SET rank=%s
    WHERE user_id=%s
    """, (rank, user_id))

    conn.commit()
    cur.close()
    conn.close()

# =========================================================
# MEMBRESÍA
# =========================================================

def is_premium(user_id: int) -> bool:
    user = get_user(user_id)
    if not user or not user["expires_at"]:
        return False
    return user["expires_at"] > datetime.utcnow()

# =========================================================
# CRÉDITOS
# =========================================================

def add_credits(user_id: int, amount: int):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    UPDATE users
    SET credits = credits + %s
    WHERE user_id=%s
    """, (amount, user_id))

    conn.commit()
    cur.close()
    conn.close()

def has_credits(user_id: int, amount: int) -> bool:
    user = get_user(user_id)
    return bool(user and user["credits"] >= amount)

def remove_credits(user_id: int, amount: int) -> bool:
    """
    Descuenta créditos SOLO si tiene suficientes.
    Retorna True si se descontó, False si no.
    """
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    UPDATE users
    SET credits = credits - %s
    WHERE user_id=%s AND credits >= %s
    """, (amount, user_id, amount))

    success = cur.rowcount > 0

    conn.commit()
    cur.close()
    conn.close()

    return success

# =========================================================
# KEYS
# =========================================================

def create_key(key: str, days: int = 0, credits: int = 0) -> bool:
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
        INSERT INTO keys (key, days, credits)
        VALUES (%s, %s, %s)
        """, (key, days, credits))

        conn.commit()
        return True

    except psycopg2.Error:
        conn.rollback()
        return False

    finally:
        cur.close()
        conn.close()

def use_key(key: str, user_id: int):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT days, credits, used
    FROM keys
    WHERE key=%s
    """, (key,))

    row = cur.fetchone()

    # ❌ key inválida o ya usada
    if not row or row["used"]:
        cur.close()
        conn.close()
        return False

    try:
        cur.execute("BEGIN")

        # Marcar key como usada
        cur.execute("""
        UPDATE keys
        SET used = TRUE
        WHERE key=%s
        """, (key,))

        # ⏳ DÍAS PREMIUM (NO TOCA RANK)
        if row["days"] > 0:
            expires = datetime.utcnow() + timedelta(days=row["days"])
            cur.execute("""
            UPDATE users
            SET expires_at = %s
            WHERE user_id = %s
            """, (expires, user_id))

        # 💳 CRÉDITOS
        if row["credits"] > 0:
            cur.execute("""
            UPDATE users
            SET credits = credits + %s
            WHERE user_id = %s
            """, (row["credits"], user_id))

        conn.commit()
        return row["days"], row["credits"]

    except Exception as e:
        conn.rollback()
        print("ERROR use_key:", e)
        return False

    finally:
        cur.close()
        conn.close()
