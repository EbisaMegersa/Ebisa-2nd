import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Bot token
TOKEN = "7313915227:AAFZGDSB6Nni_cW5XB3hZGm8tDJdvpp_SRA"

# Simulated database for users (this can be replaced by an actual database)
users_data = {}

# Function to get a user’s referral link
def get_referral_link(user_id):
    return f"https://t.me/Ebisa2bot?start={user_id}"

# Function to add referral bonus to the inviter
def add_referral_bonus(inviter_id):
    if inviter_id in users_data:
        users_data[inviter_id]['balance'] += 5  # Add $5 to the inviter's balance

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message with inline keyboard buttons."""
    user_id = update.message.from_user.id
    # Initialize user data if it doesn't exist
    if user_id not in users_data:
        users_data[user_id] = {
            'username': update.message.from_user.username,
            'balance': 0,
            'referral_count': 0
        }

    keyboard = [
        [InlineKeyboardButton("Referral Link", callback_data="referral_link")],
        [InlineKeyboardButton("Withdraw", callback_data="withdraw")],
        [InlineKeyboardButton("Profile", callback_data="profile")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hello, welcome to Ebisa Telegram bot 😊",
        reply_markup=reply_markup
    )

async def referral_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the referral link to the user."""
    user_id = update.message.from_user.id
    referral_link = get_referral_link(user_id)
    await update.message.reply_text(f"Your referral link: {referral_link}")

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check the user's balance and allow or disallow withdrawal."""
    user_id = update.message.from_user.id
    if user_id in users_data:
        balance = users_data[user_id]['balance']
        if balance < 10:
            await update.message.reply_text("You're not eligible to withdraw yet.")
        else:
            await update.message.reply_text("Wow, you're unique! You can withdraw now.")
    else:
        await update.message.reply_text("User not found.")

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the user's profile with Telegram username, ID, and balance."""
    user_id = update.message.from_user.id
    if user_id in users_data:
        user_info = users_data[user_id]
        profile_text = (
            f"Username: {user_info['username']}\n"
            f"User ID: {user_id}\n"
            f"Balance: ${user_info['balance']}"
        )
        await update.message.reply_text(profile_text)
    else:
        await update.message.reply_text("User not found.")

async def handle_referral(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the referral link used by a new user."""
    user_id = update.message.from_user.id
    if user_id in users_data:
        # Referral logic
        users_data[user_id]['referral_count'] += 1
        inviter_id = update.message.text.split()[-1]  # Assuming the user has the inviter's ID
        add_referral_bonus(inviter_id)

    await update.message.reply_text("Referral successful!")

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(referral_link, pattern="referral_link"))
    application.add_handler(CallbackQueryHandler(withdraw, pattern="withdraw"))
    application.add_handler(CallbackQueryHandler(profile, pattern="profile"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_referral))

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
