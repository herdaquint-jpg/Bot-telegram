import os
import asyncio
import threading
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# =========================
# TOKEN DEL BOT
# =========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("⚠ No se encontró el token. Configura BOT_TOKEN en Render.")

# =========================
# FLASK PARA RENDER
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot activo 🚀"

# =========================
# COMANDOS
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy tu bot y estoy funcionando 🚀")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Comandos disponibles:\n"
        "/start - Inicia el bot\n"
        "/help - Muestra esta ayuda\n"
        "Además, responde automáticamente a palabras clave como: hola, precio, info, gracias..."
    )

# =========================
# RESPUESTAS AUTOMÁTICAS
# =========================
async def auto_responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "hola" in text:
        await update.message.reply_text("¡Hola! ¿Cómo estás?")
    elif "precio" in text:
        await update.message.reply_text("Te envío la info de precios por privado 📩")
    elif "gracias" in text:
        await update.message.reply_text("¡Con gusto! 😊")
    elif "adios" in text or "chao" in text:
        await update.message.reply_text("¡Hasta pronto! 👋")
    elif "info" in text:
        await update.message.reply_text(
            "📌 Información:\n"
            "Hola soy @K1104m (ÚNICO TELEGRAM EXISTENTE)\n"
            "Cuenta de insta: @tatamoreno11\n"
            "Un mes entero mi canal privado info priv\n"
            "Contenido personalizado\n"
            "Solicitar métodos de pago.\n"
            "Contacto:  @K1104m"
        )

# =========================
# MENSAJE DE BIENVENIDA EN GRUPOS
# =========================
async def welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"🎉 Bienvenido/a {member.full_name} al grupo.")

# =========================
# MAIN DEL BOT
# =========================
async def main():
    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Comandos
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("help", help_command))

    # Respuestas automáticas
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_responder))

    # Bienvenida a nuevos miembros
    bot_app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_message))

    print("🤖 Bot iniciado y escuchando mensajes...")
    await bot_app.run_polling(close_loop=False)  # Para que no cierre el loop de Flask

# =========================
# EJECUCIÓN
# =========================
if __name__ == "__main__":
    # Flask en segundo plano
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))).start()

    # Bot en el hilo principal
    asyncio.run(main())

