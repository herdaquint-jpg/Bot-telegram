from telegram.ext import Updater, CommandHandler

def start(update, context):
    update.message.reply_text("Hola! Soy tu bot funcionando con polling en Render")

def main():
    updater = Updater("TU_TOKEN_DE_TELEGRAM")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

