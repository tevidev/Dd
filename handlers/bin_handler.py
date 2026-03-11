from telegram import Update
from telegram.ext import ContextTypes
from utils.bin_utils import get_bin_info_by_bin


async def bin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /bin 526777")
        return

    bin_number = context.args[0][:6]

    if not bin_number.isdigit() or len(bin_number) != 6:
        await update.message.reply_text("❌ BIN inválido")
        return

    info = get_bin_info_by_bin(bin_number)

    if not info:
        await update.message.reply_text("❌ BIN no encontrado")
        return

    text = (
        f"🔍 **BIN LOOKUP**\n"
        f"━━━━━━━━━━━━━━\n"
        f"🏦 **Banco:** {info['bank']}\n"
        f"💳 **Marca:** {info['scheme']} {info['brand']}\n"
        f"📌 **Tipo:** {info['type']}\n"
        f"🌍 **País:** {info['country']} {info['emoji']}"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown"
    )
