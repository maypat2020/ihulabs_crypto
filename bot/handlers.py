from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CommandHandler
from bot.utils import get_top_10_cryptos, format_crypto_data, get_crypto_signals, get_crypto_analysis, subscribe_user, get_referral_link, register_referral, get_leaderboard, format_leaderboard, get_historical_data, get_buy_sell_signals

CHOOSING, TYPING_REPLY = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu_keyboard = [
        [InlineKeyboardButton("🔝 Top 10 Cryptos", callback_data='top_10_cryptos')],
        [InlineKeyboardButton("📈 Buy/Sell Signals (Top 10)", callback_data='crypto_signals')],
        [InlineKeyboardButton("📊 Crypto Analysis", callback_data='crypto_analysis')],
        [InlineKeyboardButton("🔍 Crypto Signals (Specific Coin)", callback_data='specific_signals')],
        [InlineKeyboardButton("💸 Subscribe", callback_data='subscribe')],
        [InlineKeyboardButton("🎁 Referral Program", callback_data='referral_program')],
        [InlineKeyboardButton("🏆 Leaderboard", callback_data='leaderboard')],
    ]
    menu_markup = InlineKeyboardMarkup(menu_keyboard)

    welcome_message = (
        "Welcome to iHuLabs Crypto Bot! 🚀\n"
        "Your go-to bot for cryptocurrency market analysis and signals.\n\n"
        "Please choose an option from the menu below:"
    )
    await update.message.reply_text(welcome_message, reply_markup=menu_markup)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()

    menu_keyboard = [
        [InlineKeyboardButton("🔝 Top 10 Cryptos", callback_data='top_10_cryptos')],
        [InlineKeyboardButton("📈 Buy/Sell Signals (Top 10)", callback_data='crypto_signals')],
        [InlineKeyboardButton("📊 Crypto Analysis", callback_data='crypto_analysis')],
        [InlineKeyboardButton("🔍 Crypto Signals (Specific Coin)", callback_data='specific_signals')],
        [InlineKeyboardButton("💸 Subscribe", callback_data='subscribe')],
        [InlineKeyboardButton("🎁 Referral Program", callback_data='referral_program')],
        [InlineKeyboardButton("🏆 Leaderboard", callback_data='leaderboard')],
    ]
    menu_markup = InlineKeyboardMarkup(menu_keyboard)

    if query:
        await query.edit_message_text("Please choose an option:", reply_markup=menu_markup)
    else:
        await update.message.reply_text("Please choose an option:", reply_markup=menu_markup)

async def top_10_cryptos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    crypto_data = get_top_10_cryptos()
    if not crypto_data:
        await query.edit_message_text("Error fetching data. Please try again later.")
        return

    formatted_data = format_crypto_data(crypto_data)
    back_keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='menu')]]
    back_markup = InlineKeyboardMarkup(back_keyboard)
    await query.edit_message_text(f"Top 10 Cryptocurrencies:\n\n{formatted_data}", reply_markup=back_markup)

async def crypto_signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    signals = get_crypto_signals()
    if not signals:
        await query.edit_message_text("Error fetching signals. Please try again later.")
        return

    back_keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='menu')]]
    back_markup = InlineKeyboardMarkup(back_keyboard)
    await query.edit_message_text(f"Crypto Buy/Sell Signals:\n\n{signals}", reply_markup=back_markup)

async def ask_for_crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Please enter the cryptocurrency symbol (e.g., 'bitcoin'):")
    return TYPING_REPLY

async def specific_crypto_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coin_id = update.message.text.lower()
    analysis = get_crypto_analysis(coin_id)
    back_keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='menu')]]
    back_markup = InlineKeyboardMarkup(back_keyboard)
    await update.message.reply_text(f"Market Analysis for {coin_id}:\n\n{analysis}", reply_markup=back_markup)
    return ConversationHandler.END

async def specific_crypto_signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coin_id = update.message.text.lower()
    prices = get_historical_data(coin_id, 100)
    back_keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='menu')]]
    back_markup = InlineKeyboardMarkup(back_keyboard)
    if prices:
        signal = get_buy_sell_signals(prices)
        await update.message.reply_text(f"Buy/Sell Signal for {coin_id}:\n\nSignal: {signal}", reply_markup=back_markup)
    else:
        await update.message.reply_text(f"Error fetching data for {coin_id}.", reply_markup=back_markup)
    return ConversationHandler.END

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    success = subscribe_user(user_id)
    back_keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='menu')]]
    back_markup = InlineKeyboardMarkup(back_keyboard)
    if success:
        await query.edit_message_text("Subscription successful! 💸 Thank you for subscribing.", reply_markup=back_markup)
    else:
        await query.edit_message_text("Subscription failed. Please try again later.", reply_markup=back_markup)

async def referral_program(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    referral_link = get_referral_link(user_id)
    back_keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='menu')]]
    back_markup = InlineKeyboardMarkup(back_keyboard)
    await query.edit_message_text(f"Your referral link: {referral_link}\nShare this link with your friends!", reply_markup=back_markup)

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    leaderboard_data = get_leaderboard()
    formatted_leaderboard = format_leaderboard(leaderboard_data)
    back_keyboard = [[InlineKeyboardButton("⬅️ Back to Menu", callback_data='menu')]]
    back_markup = InlineKeyboardMarkup(back_keyboard)
    await query.edit_message_text(formatted_leaderboard, reply_markup=back_markup)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    print(f"User {user.first_name} canceled the conversation.")
    await update.message.reply_text("Bye! I hope we can talk again some day.")
    return ConversationHandler.END
