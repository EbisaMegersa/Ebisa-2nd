from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, PreCheckoutQueryHandler, MessageHandler, Filters, CallbackContext

# Replace with your bot token and payment provider token
BOT_TOKEN = "7313915227:AAFZGDSB6Nni_cW5XB3hZGm8tDJdvpp_SRA"
PAYMENT_PROVIDER_TOKEN = "YOUR_PAYMENT_PROVIDER_TOKEN"

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("Please Donate", callback_data="donate")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Hello, welcome to Ebisa Telegram bot 😊", reply_markup=reply_markup)

# Callback handler for donation
def donate(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    chat_id = query.message.chat_id
    title = "Donate 1⭐"
    description = "Support us with 1⭐. Thank you!"
    payload = "donation_payload"
    currency = "XTR"
    prices = [LabeledPrice("1⭐ Donation", 100)]  # Amount in cents (100 = 1 XTR)
    context.bot.send_invoice(
        chat_id, title, description, payload, PAYMENT_PROVIDER_TOKEN, currency, prices
    )

# Pre-checkout handler (must answer pre-checkout query)
def precheckout_callback(update: Update, context: CallbackContext) -> None:
    query = update.pre_checkout_query
    query.answer(ok=True)

# Successful payment handler
def successful_payment(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Thank you for your donation! ❤️")

# Set up the bot
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(donate, pattern="^donate$"))
    dp.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    dp.add_handler(MessageHandler(Filters.successful_payment, successful_payment))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
