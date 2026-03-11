import os
import re
from datetime import datetime
from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

TMP_DIR = "tmp_clean"
os.makedirs(TMP_DIR, exist_ok=True)

WAIT_FILE = 1


async def clean_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📂 Envíame el archivo .txt con las CC\n\n"
        "✔ Soporta separadores | / espacios\n"
        "🧹 Eliminaré las CC vencidas\n"
        "📅 Las del mes actual se conservan\n"
        "🚫 Elimina texto basura automáticamente\n"
        "🧠 Detecta y elimina duplicadas"
    )
    return WAIT_FILE


async def clean_receive_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    if not document or not document.file_name.lower().endswith(".txt"):
        await update.message.reply_text("❌ Envíame un archivo .txt válido")
        return WAIT_FILE

    await update.message.reply_text(
        "📥 Archivo recibido\n"
        "🧹 Limpiando CC, espera un momento..."
    )

    file = await document.get_file()
    uid = update.effective_user.id

    input_path = os.path.join(TMP_DIR, f"in_{uid}.txt")
    output_path = os.path.join(TMP_DIR, f"clean_{uid}.txt")

    await file.download_to_drive(input_path)

    now = datetime.now()
    current_year = now.year
    current_month = now.month

    total = 0
    removed = 0
    duplicated = 0
    valid_ccs = set()

    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            total += 1

            # Regex ultra flexible:
            # acepta | / espacios texto símbolos etc.
            match = re.search(
                r'(\d{15,16})\D+(\d{1,2})\D+(\d{2,4})\D+(\d{3,4})',
                line
            )

            if not match:
                removed += 1
                continue

            try:
                cc, mm, yy, cvv = match.groups()

                mm = int(mm)
                yy = int(yy)

                if yy < 100:
                    yy += 2000

                if not (1 <= mm <= 12):
                    removed += 1
                    continue

                if yy < current_year:
                    removed += 1
                    continue

                if yy == current_year and mm < current_month:
                    removed += 1
                    continue

                clean_cc = f"{cc}|{mm:02d}|{yy % 100:02d}|{cvv}"

                if clean_cc in valid_ccs:
                    duplicated += 1
                else:
                    valid_ccs.add(clean_cc)

            except Exception:
                removed += 1

    with open(output_path, "w", encoding="utf-8") as f:
        for cc in sorted(valid_ccs):
            f.write(cc + "\n")

    await update.message.reply_document(
        document=open(output_path, "rb"),
        filename="cc_limpias.txt",
        caption=(
            "🧹 *LIMPIEZA COMPLETADA*\n\n"
            f"📥 Total leídas: {total}\n"
            f"❌ Eliminadas (inválidas/vencidas): {removed}\n"
            f"🔁 Duplicadas eliminadas: {duplicated}\n"
            f"✅ Válidas finales: {len(valid_ccs)}"
        ),
        parse_mode="Markdown"
    )

    try:
        os.remove(input_path)
        os.remove(output_path)
    except Exception:
        pass

    return ConversationHandler.END


clean_conversation = ConversationHandler(
    entry_points=[CommandHandler("clean", clean_start)],
    states={
        WAIT_FILE: [MessageHandler(filters.Document.ALL, clean_receive_file)]
    },
    fallbacks=[],
)
