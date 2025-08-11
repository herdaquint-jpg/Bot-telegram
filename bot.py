import os
import asyncio
import threading
from flask import Flask
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes

# ==============================
#  CONFIGURACIÓN DEL BOT
# ==============================
TOKEN = os.getenv("BOT_TOKEN")  # Token desde variables de entorno en Render

if not TOKEN:
    raise ValueError("⚠️ No se encontró el token del bot. Configura BOT_TOKEN en Render.")

# ==============================
#  PALABRAS CLAVE Y RESPUESTAS
# ==============================
RESPUESTAS = {
    "hola": "¡Hola! 👋 ¿Cómo estás?",
    "precio": "💰 Escríbeme por privado para enviarte los precios.",
    "gracias": "Con gusto 😊",
    "adios": "¡Hasta luego! 👋",
    "info": "ℹ️ Soy TataMoreno y este es mi canal privado.",
}

# ==============================
#  COMANDOS DEL BOT
# ==============================
async def start(update, context):
    await update.message.reply_text(
        "¡Hola! Soy TataMoreno 🤖\n"
        "Puedes usar /help para ver los comandos disponibles."
    )

async def help_command(update, context):
    await update.message.reply_text(
        "📌 Comandos disponibles:\n"
        "/start - Inicia el bot\n"
        "/help - Muestra esta ayuda\n\n"
        "En grupos, si me mencionas o dices una palabra clave, te responderé 😎"
    )

# ==============================
#  RESPUESTA AUTOMÁTICA
# ==============================
async def responder_mensaje(update, context):
    texto = update.message.text.lower()

    # Si está en un grupo y lo mencionan
    if update.message.chat.type in ["group", "supergroup"]:
        if f"@{context.bot.username.lower()}" in texto:
            await update.message.reply_text("¡Hola! Me mencionaste en el grupo 😄")

    # Si contiene palabras clave
    for palabra, respuesta in RESPUESTAS.items():
        if palabra in texto:
            await update.message.reply_text(respuesta)
            break

# ==============================
#  MENSAJE DE BIENVENIDA
# ==============================
async def bienvenida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for usuario in update.message.new_chat_members:
        nombre = usuario.first_name
        await update.message.reply_text(
            f"🎉 ¡Bienvenido/a {nombre} al grupo!\n\n"
            "Soy TataMoreno 🤖 y estoy aquí para ayudarte.\n"
            "Escribe *info* para más detalles 😉",
            parse_mode="Markdown"
        )

# ==============================
#  LÓGICA DEL BOT
# ==============================
async def main_bot():
    app_bot = ApplicationBuilder().token(TOKEN).build()

    # Comandos
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("help", help_command))

    # Responder mensajes
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_mensaje))

    # Bienvenida automática
    app_bot.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, bienvenida))

    print("✅ Bot iniciado y esperando mensajes...")
    await app_bot.run_polling()

def run_bot_thread():
    asyncio.run(main_bot())

# ==============================
#  SERVIDOR FLASK PARA RENDER
# ==============================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot activo ✅"

# ==============================
#  INICIO PRINCIPAL
# ==============================
if __name__ == "__main__":
    # Inicia el bot en un hilo separado
    threading.Thread(target=run_bot_thread, daemon=True).start()

    # Inicia Flask en el puerto asignado por Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
