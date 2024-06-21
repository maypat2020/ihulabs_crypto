from telegram.ext import CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
from bot.handlers import start, menu, top_10_cryptos, crypto_signals, ask_for_crypto, specific_crypto_analysis, specific_crypto_signals, subscribe, referral_program, leaderboard, cancel
from bot.handlers import CHOOSING, TYPING_REPLY  # Import the state variables

def setup_handlers(application):
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('menu', menu))  # Add menu command
    application.add_handler(CallbackQueryHandler(menu, pattern='menu'))
    application.add_handler(CallbackQueryHandler(top_10_cryptos, pattern='top_10_cryptos'))
    application.add_handler(CallbackQueryHandler(crypto_signals, pattern='crypto_signals'))
    
    # Conversation handler for specific crypto analysis
    analysis_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(ask_for_crypto, pattern='crypto_analysis')],
        states={
            TYPING_REPLY: [MessageHandler(filters.TEXT & ~filters.COMMAND, specific_crypto_analysis)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(analysis_handler)
    
    # Conversation handler for specific crypto signals
    signals_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(ask_for_crypto, pattern='specific_signals')],
        states={
            TYPING_REPLY: [MessageHandler(filters.TEXT & ~filters.COMMAND, specific_crypto_signals)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(signals_handler)
    
    application.add_handler(CallbackQueryHandler(subscribe, pattern='subscribe'))
    application.add_handler(CallbackQueryHandler(referral_program, pattern='referral_program'))
    application.add_handler(CallbackQueryHandler(leaderboard, pattern='leaderboard'))
