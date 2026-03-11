from telegram import Update
from telegram.ext import ContextTypes
import secrets
from datetime import datetime

from database.db import (
    create_key,
    use_key,
    get_user,
    get_db,
    DB_LOCK,
    add_credits,
    set_rank,
)

from utils.roles import (
    is_owner,
    is_privileged,
    can_manage_credits,
)
from database.db import set_rank, register_user

# =====================================================
# 🔑 CREAR KEY (OWNER + SELLER)
# =====================================================
async def genkey(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_privileged(update.effective_user.id):
        await update.message.reply_text("❌ No tienes permisos para generar keys")
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Uso:\n/genkey <días> <créditos>\nEj: /genkey 7 50"
        )
        return

    try:
        days = int(context.args[0])
        credits = int(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ Días y créditos deben ser números")
        return

    key = secrets.token_hex(8).upper()

    if not create_key(key, days, credits):
        await update.message.reply_text("❌ Error: la key ya existe")
        return

    await update.message.reply_text(
        f"✅ *Key generada*\n\n"
        f"🔑 `{key}`\n"
        f"📅 Días: `{days}`\n"
        f"💳 Créditos: `{credits}`",
        parse_mode="Markdown"
    )


# =====================================================
# 🎟 CANJEAR KEY (USUARIOS)
# =====================================================
async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Uso: /redeem <key>")
        return

    key = context.args[0]
    user_id = update.effective_user.id

    result = use_key(key, user_id)
    if not result:
        await update.message.reply_text("❌ Key inválida o ya usada")
        return

    days, credits = result

    msg = "✅ *Beneficios activados*\n\n"
    if days > 0:
        msg += f"📆 Membresía: `{days}` días\n"
    if credits > 0:
        msg += f"💳 Créditos: `{credits}`\n"

    await update.message.reply_text(msg, parse_mode="Markdown")


# =====================================================
# 💳 AGREGAR CRÉDITOS (OWNER + SELLER)
# =====================================================
async def addcredits(update: Update, context: ContextTypes.DEFAULT_TYPE):
    actor = update.effective_user

    if not can_manage_credits(actor.id):
        await update.message.reply_text("❌ No tienes permisos para agregar créditos")
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Uso:\n/addcredits <user_id> <cantidad>\nEj: /addcredits 123456 50"
        )
        return

    try:
        user_id = int(context.args[0])
        amount = int(context.args[1])
    except ValueError:
        await update.message.reply_text("❌ Datos inválidos")
        return

    user = get_user(user_id)
    if not user:
        await update.message.reply_text("❌ Usuario no registrado")
        return

    # ➕ Agregar créditos (transacción segura)
    with DB_LOCK:
        conn = get_db()
        add_credits(conn, user_id, amount)
        conn.commit()
        conn.close()

    actor_role = "👑 OWNER" if is_owner(actor.id) else "🛒 SELLER"

    # ✅ Confirmación al ejecutor
    await update.message.reply_text(
        f"✅ *Créditos agregados*\n\n"
        f"🆔 Usuario: `{user_id}`\n"
        f"💳 +{amount} créditos\n"
        f"👤 Por: {actor_role}",
        parse_mode="Markdown"
    )

    # 📩 MENSAJE PRO AL USUARIO
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "💳 *CRÉDITOS RECIBIDOS*\n"
                "━━━━━━━━━━━━━━━━━━\n"
                f"➕ *+{amount} créditos*\n"
                f"👤 Otorgado por: {actor_role}\n"
                f"🕒 {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
                "🔥 Ya puedes usar funciones premium\n"
                "🤖 *DIANE BOT*"
            ),
            parse_mode="Markdown"
        )
    except Exception:
        pass


# =====================================================
# 🛒 AGREGAR SELLER (SOLO OWNER)
# =====================================================
async def addseller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("❌ Solo el OWNER puede hacer esto")
        return

    if not context.args:
        await update.message.reply_text("Uso: /addseller <user_id>")
        return

    user_id = int(context.args[0])

    # ✅ ASEGURAR QUE EL USUARIO EXISTE EN BD
    register_user(user_id, None)

    # 🛒 ASIGNAR RANGO SELLER
    set_rank(user_id, "SELLER")

    await update.message.reply_text("✅ SELLER agregado correctamente")

    # 📩 MENSAJE PRIVADO AL SELLER
    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "🎉 *¡FELICIDADES!*\n\n"
                "Has sido ascendido a 🧑‍💼 *SELLER*\n\n"
                "Ahora tienes acceso a:\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "🔑 `/genkey <días> <créditos>`\n"
                "💳 `/addcredits <user_id> <cantidad>`\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
                "⚠️ Puedes usar el bot sin membresía ni créditos\n"
                "📌 Usa los comandos con responsabilidad\n\n"
                "🤖 *DIANE BOT*"
            ),
            parse_mode="Markdown"
        )
    except Exception:
        await update.message.reply_text(
            "⚠️ SELLER agregado, pero no se pudo enviar mensaje privado\n"
            "📌 El usuario debe iniciar el bot primero"
        )


# =====================================================
# 🚫 REMOVER SELLER (SOLO OWNER)
# =====================================================
async def banseller(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_owner(update.effective_user.id):
        await update.message.reply_text("❌ Solo el OWNER puede hacer esto")
        return

    if not context.args:
        await update.message.reply_text("Uso: /banseller <user_id>")
        return

    user_id = int(context.args[0])
    set_rank(user_id, "USER")

    await update.message.reply_text("🚫 SELLER removido correctamente")

    try:
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "🚫 *CAMBIO DE RANGO*\n\n"
                "Tu acceso como SELLER ha sido revocado\n\n"
                "🔒 Ya no puedes:\n"
                "• Crear keys\n"
                "• Agregar créditos\n\n"
                "📌 Para funciones premium\n"
                "necesitarás membresía o créditos\n\n"
                "🤖 *DIANE BOT*"
            ),
            parse_mode="Markdown"
        )
    except Exception:
        pass
