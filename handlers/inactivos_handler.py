from telegram import Update
from telegram.ext import ContextTypes
from database.db import get_inactive_users
from utils.roles import is_privileged


async def inactivos_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_privileged(update.effective_user.id):
        return

    users = get_inactive_users(30)

    await update.message.reply_text(
        f"💀 Usuarios inactivos +30 días: {len(users)}"
    )
