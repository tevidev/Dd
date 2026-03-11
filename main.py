import os

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from handlers.clean_handler import clean_conversation
from handlers.txt_handler import txt_conversation
from handlers.bin_handler import bin_handler
from handlers.gen import gen_handler
from handlers.gates_handler import gate_handler, GATES, stop_process_callback
from handlers.cookie_handler import cookie_handler, cookie_file_handler

from menu import (
    menu_principal,
    menu_gates,
    menu_tools,
    menu_info,
)

from database.db import init_db

from auth.register import register
from auth.info import info

from auth.admin import (
    genkey,
    redeem,
    addcredits,
    addseller,
    banseller,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def on_startup(app):
    await app.bot.delete_webhook(drop_pending_updates=True)


def main():

    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN no configurado")

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .concurrent_updates(True)
        .post_init(on_startup)
        .build()
    )

    # 🔹 Inicializar base de datos
    init_db()

    # =============================
    # 🔴 CONVERSACIONES (PRIMERO)
    # =============================

    app.add_handler(clean_conversation)
    app.add_handler(txt_conversation)

    # =============================
    # 🔵 COMANDOS BÁSICOS
    # =============================

    app.add_handler(CommandHandler("start", menu_principal))
    app.add_handler(CommandHandler("cmds", menu_principal))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("id", info))

    # =============================
    # 🔵 ADMIN
    # =============================

    app.add_handler(CommandHandler("genkey", genkey))
    app.add_handler(CommandHandler("redeem", redeem))
    app.add_handler(CommandHandler("addcredits", addcredits))
    app.add_handler(CommandHandler("addseller", addseller))
    app.add_handler(CommandHandler("banseller", banseller))

    # =============================
    # 🔵 GATES
    # =============================

    for gate in GATES:
        app.add_handler(CommandHandler(gate, gate_handler))

    # =============================
    # 🔵 HERRAMIENTAS
    # =============================

    app.add_handler(CommandHandler("gen", gen_handler))
    app.add_handler(CommandHandler("bin", bin_handler))

    # =============================
    # 🍪 COOKIE SYSTEM
    # =============================

    app.add_handler(CommandHandler("cookie", cookie_handler))

    # recibe archivo de cookie
    app.add_handler(
        MessageHandler(filters.Document.ALL, cookie_file_handler)
    )

    # =============================
    # 🛑 BOTÓN STOP PROCESS
    # =============================

    app.add_handler(
        CallbackQueryHandler(stop_process_callback, pattern="stop_process")
    )

    # =============================
    # 📋 MENÚS
    # =============================

    app.add_handler(
        CallbackQueryHandler(menu_gates, pattern="menu_gates")
    )

    app.add_handler(
        CallbackQueryHandler(menu_tools, pattern="menu_tools")
    )

    app.add_handler(
        CallbackQueryHandler(menu_info, pattern="menu_info")
    )

    app.add_handler(
        CallbackQueryHandler(menu_principal, pattern="menu_inicio")
    )

    # =============================
    # 🚀 START BOT
    # =============================

    print("✅ BOT INICIADO")

    app.run_polling()


if __name__ == "__main__":
    main()
