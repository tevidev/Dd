from telegram import Update
from telegram.ext import ContextTypes
from database.db import get_active_users
from utils.roles import is_privileged
from utils.time_utils import tiempo_relativo


async def activos_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_privileged(update.effective_user.id):
        return

    users = get_active_users(10)

    if not users:
        await update.message.reply_text("No hay usuarios online.")
        return

    msg = "🟢 Usuarios Online\n\n"

    for u in users:
        msg += f"@{u.get('username','-')} — {tiempo_relativo(u.get('last_seen'))}\n"

    await update.message.reply_text(msg)
