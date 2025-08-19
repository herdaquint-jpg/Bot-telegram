import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Configurar logs (para ver errores en Render)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")  # recuerda definirlo en Render → Environment

# --- Comandos ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hola! Soy tu bot y estoy en línea 🚀")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ℹ️ Estos son los comandos disponibles:\n/start - iniciar\n/help - ayuda")

# --- Mensajes de texto ---
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🔁 Dijiste: {update.message.text}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers de comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Handler para cualquier texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Arrancar bot
    app.run_polling()

if __name__ == "__main__":
    main()
