from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from handlers.gates_handler import GATES
from utils.roles import is_privileged
from utils.roles import is_owner, is_seller, is_privileged
from database.db import get_user
from database.db import get_user
from utils.roles import is_owner
# ---------- MENÚ PRINCIPAL ----------
async def menu_principal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    text = (
        f"👋 *Bienvenido al menú de comandos*\n\n"
        f"👤 Usuario: `{user.first_name}`\n"
        f"🆔 ID: `{user.id}`\n\n"
        f"Selecciona una opción:"
    )

    keyboard = [
        [InlineKeyboardButton("🚪 Gates", callback_data="menu_gates")],
        [InlineKeyboardButton("🛠 Tools", callback_data="menu_tools")],
        [InlineKeyboardButton("ℹ️ Información", callback_data="menu_info")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            text, reply_markup=reply_markup, parse_mode="Markdown"
        )
    else:
        await update.callback_query.edit_message_text(
            text, reply_markup=reply_markup, parse_mode="Markdown"
        )


# ---------- SUBMENÚ GATES ----------
async def menu_gates(update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not GATES:
        text = (
            "🚪 *GATES DISPONIBLES*\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "❌ No hay gates activos.\n"
            "━━━━━━━━━━━━━━━━━━━"
        )
    else:
        gates_lines = []
        for gate in GATES.keys():
            emoji = "🧠" if gate == "redy" else "⚡"
            gates_lines.append(f"{emoji} *{gate.upper()}*  →  `/{gate}`")

        gates_text = "\n".join(gates_lines)

        text = (
            "🚪 *GATES DISPONIBLES*\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"{gates_text}\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            "📌 *Uso:*\n"
            "`/gate cc|mm|yy|cvv`\n\n"
            "💡 Máx *1000 CC* por comando\n"
            "⚠️ Secuencial / Multi-usuario"
        )

    keyboard = [
        [InlineKeyboardButton("⬅️ Regresar", callback_data="menu_inicio")]
    ]

    try:
        await query.edit_message_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
    except BadRequest as e:
        if "Message is not modified" not in str(e):
            raise e

# ---------- SUBMENÚ TOOLS ----------
async def menu_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🛠 *Tools disponibles*\n\n"
        "• BIN Checker\n"
        "• Email Validator\n"
        "• Proxy Tester\n"
    )

    keyboard = [
        [InlineKeyboardButton("⬅️ Regresar", callback_data="menu_inicio")]
    ]

    await update.callback_query.edit_message_text(
        text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
    )


# ---------- INFORMACIÓN DEL USUARIO ----------
async def menu_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db_user = get_user(user.id)

    if is_owner(user.id):
        role = "👑 OWNER"
    elif is_seller(user.id):
        role = "🛒 SELLER"
    else:
        role = "👤 USER"

    text = (
        "ℹ️ *Información del usuario*\n\n"
        f"👤 Nombre: `{user.first_name}`\n"
        f"👥 Username: `{user.username}`\n"
        f"🆔 ID: `{user.id}`\n"
        f"🎖 Rol: *{role}*\n"
        f"🤖 Bot: `{context.bot.username}`"
    )

    keyboard = [
        [InlineKeyboardButton("⬅️ Regresar", callback_data="menu_inicio")]
    ]

    await update.callback_query.edit_message_text(
        text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )