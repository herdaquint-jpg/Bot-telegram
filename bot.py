import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Configuración de logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No se encontró la variable BOT_TOKEN")

last_messages = {}

# --- Comandos ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hola, soy tu bot. Usa /ayuda para más info.")

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Comandos:\n/start - Inicia el bot\n/ayuda - Muestra este mensaje\n/info - Información del bot"
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot activo en Render usando python-telegram-bot 20.x")

# --- Auto respuestas ---
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.lower()

    if last_messages.get(user_id) == text:
        return
    last_messages[user_id] = text

    if "hola" in text:
        await update.message.reply_text("¡Hola! 👋")
    elif "gracias" in text:
        await update.message.reply_text("¡De nada! 😊")
    elif "adiós" in text or "chao" in text:
        await update.message.reply_text("¡Hasta pronto! 👋")

# --- Bienvenida ---
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f"🎉 Bienvenido/a {member.first_name}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

    logger.info("✅ Bot iniciado...")
    app.run_polling()

if __name__ == "__main__":
    main()

