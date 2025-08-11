from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

TOKEN = "AQUI_VA_TU_TOKEN"  # O usa Environment Variables

# Tabla de respuestas automáticas
RESPUESTAS = {
    # Saludos
    "hola": "¡Hola! 😄 ¿Cómo estás?",
    "buenos días": "¡Muy buenos días! ☀️",
    "buenas tardes": "¡Buenas tardes! 🌇",
    "buenas noches": "¡Buenas noches! 🌙",
    "qué tal": "¡Todo bien! ¿Y tú? 😊",

    # Información
    "información": (
        "📌 Hola soy @K1104m (ÚNICO TELEGRAM EXISTENTE)\n"
        "📷 Instagram: @tatamoreno11\n"
        "💬 Contenido personalizado\n"
        "💳 Solicita métodos de pago."
    ),
    "info": (
        "📌 Hola soy @K1104m (ÚNICO TELEGRAM EXISTENTE)\n"
        "📷 Instagram: @tatamoreno11\n"
        "💬 Contenido personalizado\n"
        "💳 Solicita métodos de pago."
    ),

    # Precios
    "precios": "💰 Escríbeme por privado para enviarte la lista de precios.",
    "tarifas": "💰 Escríbeme por privado para enviarte la lista de precios.",
    "cuánto vale": "💰 Escríbeme por privado para enviarte la lista de precios.",
    "valor": "💰 Escríbeme por privado para enviarte la lista de precios.",

    # Agradecimientos
    "gracias": "¡Con gusto! 💕",
    "muchas gracias": "¡De nada! 😊",
    "mil gracias": "Siempre a la orden 💖",

    # Despedidas
    "adiós": "¡Hasta luego! 👋",
    "hasta luego": "¡Nos vemos! 🙌",
    "chao": "¡Chao! 🌸",

    # Otros
    "ok": "👌",
    "listo": "Perfecto ✅",
    "perfecto": "Genial 😎"
}

# Comando /start
async def start(update, context):
    await update.message.reply_text(
        "¡Hola! 👋 Soy TataMorenoBot.\n"
        "Puedes escribirme palabras como:\n"
        "- hola / buenos días / buenas tardes\n"
        "- información / info\n"
        "- precios / tarifas / cuánto vale / valor\n"
        "- gracias / muchas gracias\n"
        "- adiós / hasta luego / chao"
    )

# Función de respuesta automática
async def responder(update, context):
    texto = update.message.text.lower().strip()

    for clave, respuesta in RESPUESTAS.items():
        if clave in texto:
            await update.message.reply_text(respuesta)
            return

    await update.message.reply_text(
        "No entiendo muy bien 🤔, pero puedes pedirme 'información' o 'precios'."
    )

# Función principal
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.run_polling()

if __name__ == "__main__":
    main()
