import logging
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Set your OpenAI API key
openai.api_key = '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'

# Set your Telegram Bot token
TELEGRAM_TOKEN = '7313915227:AAFZGDSB6Nni_cW5XB3hZGm8tDJdvpp_SRA'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    await update.message.reply_text("Hello! I'm your ChatGPT assistant. Type any question or message, and I'll respond!")

async def chatgpt_response(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the user message to ChatGPT and return the response."""
    user_message = update.message.text
    try:
        # Get a response from ChatGPT
        response = openai.Completion.create(
            model="gpt-4",  # Use the appropriate model, you can also use "gpt-3.5-turbo"
            prompt=user_message,
            max_tokens=150
        )
        bot_reply = response.choices[0].text.strip()
        await update.message.reply_text(bot_reply)
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("Sorry, something went wrong. Please try again later.")

def main() -> None:
    """Start the Telegram bot."""
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chatgpt_response))

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
