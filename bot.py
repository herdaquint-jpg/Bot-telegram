import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# ==============================
# CONFIGURACIÓN DE LOGS
# ==============================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ==============================
# TOKEN DEL BOT
# ==============================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN no está configurado en las variables de entorno")

# ==============================
# MANEJADORES DE COMANDOS
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mensaje de bienvenida."""
    await update.message.reply_text(
        "👋 ¡Hola! Soy tu bot en Render con python-telegram-bot 20.x 🚀\n\n"
        "Escribe /help para ver lo que puedo hacer."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Lista de comandos disponibles."""
    await update.message.reply_text(
        "📚 *Comandos disponibles:*\n"
        "/start - Iniciar el bot\n"
        "/help - Mostrar esta ayuda\n"
        "/about - Información sobre el bot\n\n"
        "💬 También puedo responder a cualquier mensaje de texto que envíes.",
        parse_mode="Markdown"
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Información sobre el bot."""
    await update.message.reply_text(
        "🤖 *Acerca de este bot:*\n"
        "Este bot fue creado para ejecutarse en Render usando python-telegram-bot 20.x.\n"
        "Soporta comandos, respuestas automáticas y manejo de errores.",
        parse_mode="Markdown"
    )

# ==============================
# RESPUESTA A MENSAJES DE TEXTO
# ==============================
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde a mensajes de texto que no son comandos."""
    user_text = update.message.text
    await update.message.reply_text(f"📩 Recibí tu mensaje: {user_text}")

# ==============================
# MANEJO DE ERRORES
# ==============================
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Maneja errores globales del bot."""
    logging.error("⚠️ Error en el bot:", exc_info=context.error)
    if isinstance(update, Update) and update.message:
        await update.message.reply_text(
            "⚠️ Ocurrió un error al procesar tu solicitud. Inténtalo más tarde."
        )

# ==============================
# FUNCIÓN PRINCIPAL
# ==============================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about_command))

    # Mensajes de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Manejo de errores
    app.add_error_handler(error_handler)

    logging.info("✅ Bot iniciado y escuchando mensajes...")
    app.run_polling()

# ==============================
# EJECUCIÓN
# ==============================
if __name__ == "__main__":
    main()
