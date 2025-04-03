import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot token
TOKEN = "7313915227:AAFZGDSB6Nni_cW5XB3hZGm8tDJdvpp_SRA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message with donation button when /start is issued."""
    keyboard = [
        [InlineKeyboardButton("Please Donate", callback_data='donate')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        'Hello, welcome to Ebisa Telegram Bot 😊',
        reply_markup=reply_markup
    )

async def donate_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the donation button press and send an invoice."""
    query = update.callback_query
    await query.answer()

    # Create a test invoice
    title = "Donation to Ebisa Bot"
    description = "Thank you for supporting our bot! This donation helps us keep the service running."
    payload = "donation-payload"
    currency = "XTR"  # Using XTR as our custom currency
    prices = [{"label": "1⭐ Star Donation", "amount": 100}]  # Amount in smallest currency unit (e.g., cents)

    # For actual payments, you would need a payment provider token
    # provider_token = "YOUR_PAYMENT_PROVIDER_TOKEN"  # Required for real payments
    provider_token = "TEST_TOKEN"  # Works only in test mode

    await context.bot.send_invoice(
        chat_id=query.message.chat_id,
        title=title,
        description=description,
        payload=payload,
        provider_token=provider_token,
        currency=currency,
        prices=prices,
        need_name=True,
        need_email=True,
        need_phone_number=False,
        need_shipping_address=False,
        is_flexible=False,
        start_parameter="donation"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message and send a greeting."""
    user_name = update.message.from_user.first_name
    greeting = f"Hello {user_name}! Thanks for your message: {update.message.text}"
    await update.message.reply_text(greeting)

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(donate_callback, pattern='^donate$'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
