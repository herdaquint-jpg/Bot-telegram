from flask import Flask
import threading
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import os

# -----------------------------
# Servidor web para Render
# -----------------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot de Telegram funcionando ✅"

def run_web():
    app.run(host='0.0.0.0', port=10000)

# -----------------------------
# Funciones del Bot
# -----------------------------
async def start(update, context):
    await update.message.reply_text("Hola 👋, soy tu bot y estoy activo.")

async def responder(update, context):
    mensaje = update.message.text.lower()

    # Ejemplos de respuestas automáticas
    if "hola" in mensaje:
        await update.message.reply_text("¡Hola! ¿Cómo estás?")
    elif "adiós" in mensaje or "chao" in mensaje:
        await update.message.reply_text("¡Hasta luego! 👋")
    elif "precio" in mensaje:
        await update.message.reply_text("Envíame un mensaje privado para enviarte la lista de precios 📋")
    else:
        await update.message.reply_text("Recibí tu mensaje 😉")

# -----------------------------
# Inicializar Bot y Web
# -----------------------------
async def main():
    token = os.getenv("TELEGRAM_TOKEN")  # Usa variable de entorno
    app_bot = ApplicationBuilder().token(token).build()

    # Comandos
    app_bot.add_handler(CommandHandler("start", start))

    # Responder a cualquier mensaje en grupos
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print("Bot iniciado ✅")
    await app_bot.run_polling()

if __name__ == '__main__':
    # Iniciar servidor web en un hilo
    web_thread = threading.Thread(target=run_web)
    web_thread.start()

    # Iniciar bot
    import asyncio
    asyncio.run(main())
