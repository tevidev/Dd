from telegram import Update
from telegram.ext import ContextTypes
import os

# ===============================
# COMANDO /cookie
# ===============================
async def cookie_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["waiting_cookie"] = True

    await update.message.reply_text(
        "📂 Envíame el archivo `.txt` con la cookie de Amazon",
        parse_mode="Markdown"
    )


# ===============================
# RECIBIR ARCHIVO
# ===============================
async def cookie_file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # verificar si el bot está esperando cookie
    if not context.user_data.get("waiting_cookie"):
        return

    if not update.message.document:
        return

    document = update.message.document

    if not document.file_name.endswith(".txt"):
        await update.message.reply_text("❌ El archivo debe ser .txt")
        return

    # mensaje inicial
    msg = await update.message.reply_text("⚙️ Configurando cookie...")

    file = await document.get_file()

    os.makedirs("cookies", exist_ok=True)

    path = f"cookies/{update.effective_user.id}.txt"

    await file.download_to_drive(path)

    # leer cookie
    with open(path, "r", encoding="utf-8") as f:
        cookie = f.read().strip()

    context.user_data["amazon_cookie"] = cookie

    # ya no esperar cookie
    context.user_data["waiting_cookie"] = False

    # editar mensaje
    await msg.edit_text("✅ Cookie configurada correctamente 🍪")
