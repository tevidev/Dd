from telegram import Update
from telegram.ext import ContextTypes
from utils.gen_template import generate_from_template

async def gen_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "Uso:\n/gen 52677752089xxxxx|02|rnd|rnd"
        )
        return

    template = context.args[0]

    try:
        cards = generate_from_template(template, amount=10)
    except Exception:
        await update.message.reply_text("❌ Formato inválido")
        return

    text = (
        "🧪 *BIN GENERATOR*\n"
        "━━━━━━━━━━━━━━\n"
        + "\n".join(cards) +
        "\n━━━━━━━━━━━━━━\n"
        
    )

    await update.message.reply_text(text, parse_mode="Markdown")
