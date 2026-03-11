from telegram import Update
from telegram.ext import ContextTypes
from database.db import register_user, get_user

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if get_user(user.id):
        await update.message.reply_text("⚠️ Ya estás registrado")
        return

    register_user(user.id, user.username)
    await update.message.reply_text("✅ Registro exitoso")
