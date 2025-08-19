import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Configuración de logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Token desde Render (variables de entorno)
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN no está configurado en Render")

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde al comando /start"""
    await update.message.reply_text("👋 Hola, estoy corriendo en Render con PTB 20.6 🚀")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde al comando /help"""
    await update.message.reply_text("📖 Comandos disponibles:\n/start - Iniciar\n/help - Ayuda")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde repitiendo cualquier texto"""
    await update.message.reply_text(f"📩 Recibí: {update.message.text}")

# --- Main ---
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers de comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Responde a cualquier texto que no sea comando
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logging.info("✅ Bot iniciado con polling en Render...")
    app.run_polling()

if __name__ == "__main__":
    main()
