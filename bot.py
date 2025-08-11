import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Configuración de logs (útil para depuración en Render)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Cargar el token desde variable de entorno
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("⚠️ No se encontró la variable BOT_TOKEN en el entorno.")

# Diccionario para registrar últimos mensajes y evitar spam
last_messages = {}

# -------- Comandos --------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ¡Hola! Soy tu bot de Telegram.\nEscribe /ayuda para ver lo que puedo hacer."
    )

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Comandos disponibles:\n"
        "/start - Iniciar conversación\n"
        "/ayuda - Mostrar esta ayuda\n"
        "/info - Información sobre el bot\n"
        "\n💬 También respondo a mensajes con palabras clave como 'hola', 'gracias', 'adiós'."
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot de ejemplo para responder automáticamente en grupos y chats privados."
    )

# -------- Respuestas automáticas --------
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.lower()

    # Anti-spam: no responder dos veces seguidas lo mismo al mismo usuario
    if last_messages.get(user_id) == text:
        return
    last_messages[user_id] = text

    if "hola" in text:
        await update.message.reply_text("¡Hola! 👋")
    elif "gracias" in text:
        await update.message.reply_text("¡De nada! 😊")
    elif "adiós" in text or "chao" in text:
        await update.message.reply_text("¡Hasta luego! 👋")
    elif "bot" in text:
        await update.message.reply_text("Sí, aquí estoy 🤖")

# -------- Bienvenida --------
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"🎉 Bienvenido/a {member.first_name} al grupo.")

# -------- Main --------
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("info", info))

    # Bienvenida
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))

    # Respuestas automáticas a mensajes
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    logger.info("✅ Bot iniciado y ejecutándose...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

