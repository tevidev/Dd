from telegram import Update
from telegram.ext import ContextTypes
from database.db import get_user
from datetime import datetime


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    if not user:
        await update.message.reply_text("❌ No estás registrado")
        return

    # ✅ EXTRAER DESDE DICCIONARIO
    user_id = user["user_id"]
    username = user["username"]
    rank = user["rank"]
    credits = user["credits"]
    expires_at = user["expires_at"]

    # ✅ expires_at YA ES datetime
    if expires_at:
        expires = expires_at.strftime("%d/%m/%Y")
    else:
        expires = "Sin membresía"

    text = (
        "👤 *Información del usuario*\n\n"
        f"🆔 ID: `{user_id}`\n"
        f"👤 Usuario: `{username or 'Sin username'}`\n"
        f"👑 Rango: `{rank}`\n"
        f"💳 Créditos: `{credits}`\n"
        f"⏳ Expira: `{expires}`"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown"
    )
