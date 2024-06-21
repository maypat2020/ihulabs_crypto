from telegram.ext import ApplicationBuilder
from config.settings import TELEGRAM_BOT_TOKEN
from bot.commands import setup_handlers

def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    setup_handlers(application)

    print("Bot started. Press Ctrl+C to stop.")
    
    application.run_polling()

if __name__ == '__main__':
    main()
