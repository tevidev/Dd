from telegram import Update
from telegram.ext import ContextTypes
from utils.roles import is_owner
from database.db import get_db

async def membresias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("❌ Solo owner")
        return

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT user_id, username, rank, credits, expires_at, last_seen
    FROM users
    ORDER BY last_seen DESC NULLS LAST
    LIMIT 50
    """)

    users = cur.fetchall()

    cur.close()
    conn.close()

    if not users:
        await update.message.reply_text("No hay usuarios")
        return

    msg = "👑 Usuarios del bot\n\n"

    for u in users:
        msg += f"""
ID: {u['user_id']}
User: @{u['username']}
Rank: {u['rank']}
Credits: {u['credits']}
"""
    await update.message.reply_text(msg[:4000])
