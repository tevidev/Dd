import asyncio
from telegram import Update
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
)

from handlers.gates_handler import procesar_ccs  # reutilizamos tu lógica
from handlers.gates_handler import GATES, MAX_CCS


# -------- ESTADOS --------
ESPERANDO_ARCHIVO = 1
ESPERANDO_GATE = 2
# -------------------------


# /txt
async def txt_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📄 Envíame el archivo .txt con las CC"
    )
    return ESPERANDO_ARCHIVO


# Recibir archivo
async def recibir_archivo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    if not document:
        await update.message.reply_text("❌ Debes enviar un archivo .txt")
        return ESPERANDO_ARCHIVO

    if not document.file_name.lower().endswith(".txt"):
        await update.message.reply_text("❌ El archivo debe ser .txt")
        return ESPERANDO_ARCHIVO

    file = await document.get_file()
    path = f"/tmp/{document.file_unique_id}.txt"
    await file.download_to_drive(path)

    context.user_data["txt_path"] = path

    gates_disponibles = ", ".join(GATES.keys())

    await update.message.reply_text(
        "✅ Archivo recibido\n\n"
        "Ahora dime con qué gate procesar:\n"
        f"`{gates_disponibles}`",
        parse_mode="Markdown"
    )

    return ESPERANDO_GATE


# Recibir gate
async def recibir_gate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    comando = update.message.text.lower().strip()

    if comando not in GATES:
        await update.message.reply_text("❌ Gate no válido, intenta de nuevo")
        return ESPERANDO_GATE

    # Leer CCs
    try:
        with open(context.user_data["txt_path"], "r", encoding="utf-8") as f:
            cc_list = f.read().replace(",", "\n").splitlines()
    except Exception:
        await update.message.reply_text("❌ Error leyendo el archivo")
        return ConversationHandler.END

    cc_list = [cc.strip() for cc in cc_list if cc.strip()][:MAX_CCS]

    if not cc_list:
        await update.message.reply_text("❌ El archivo está vacío")
        return ConversationHandler.END

    # 🔥 Llamamos a TU procesador
    await procesar_ccs(update, context, cc_list, comando)

    context.user_data.clear()
    return ConversationHandler.END


# ConversationHandler
txt_conversation = ConversationHandler(
    entry_points=[CommandHandler("txt", txt_start)],
    states={
        ESPERANDO_ARCHIVO: [
            MessageHandler(filters.Document.ALL, recibir_archivo)
        ],
        ESPERANDO_GATE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_gate)
        ],
    },
    fallbacks=[],
)
