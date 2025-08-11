from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

import os
TOKEN = os.getenv("BOT_TOKEN")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = update.message.text.lower()

    # Ejemplo de respuesta automática
    if "hola" in mensaje:
        await update.message.reply_text("¡Hola! 👋 Soy el bot del grupo.")
    elif "gracias" in mensaje:
        await update.message.reply_text("¡De nada! 😊")
    else:
        await update.message.reply_text("No entendí, pero aquí estoy 🤖")

app = ApplicationBuilder().token(TOKEN).build()

# Escucha todos los mensajes que no son comandos
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

print("✅ Bot escuchando mensajes en grupo...")
app.run_polling()
