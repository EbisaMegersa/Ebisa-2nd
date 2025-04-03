import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, ShippingOption
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot token
TOKEN = "7313915227:AAFZGDSB6Nni_cW5XB3hZGm8tDJdvpp_SRA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message with an inline keyboard."""
    keyboard = [
        [InlineKeyboardButton("Denote", callback_data="denote")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hello, welcome to Ebisa Telegram bot 😊",
        reply_markup=reply_markup
    )

async def denote(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send an invoice-like message with XTR currency (1⭐)."""
    # Invoices are generally for payment, but Telegram does not support custom currencies.
    # We'll simulate the invoice with a message and the label 'XTR' as currency.

    title = "Donation for Ebisa Bot"
    description = "Your generous donation helps keep the bot running."
    payload = "XTR_CURRENCY_DONATION"
    provider_token = "YOUR_PROVIDER_TOKEN"  # Replace this with your provider token
    start_parameter = "donate_xtr"

    prices = [LabeledPrice("1⭐", 100)]  # Amount 1⭐ (use 100 for 1⭐ equivalent)
    
    try:
        await update.message.reply_invoice(
            title=title,
            description=description,
            payload=payload,
            provider_token=provider_token,
            start_parameter=start_parameter,
            prices=prices
        )
    except Exception as e:
        logging.error(f"Error sending invoice: {e}")
        await update.message.reply_text("There was an issue sending the invoice. Please try again later.")

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
    application.add_handler(CallbackQueryHandler(denote, pattern="denote"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
