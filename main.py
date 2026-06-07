import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters

# Import the handlers from our bot module
from Telegram_Bot_Trigger import start_command, handle_message_with_search, handle_approval


def main():
    load_dotenv()

    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        print("Error: TELEGRAM_TOKEN is missing. Please check your .env file.")
        return

    print("Starting Multi-Agent System Core...")

    # Initialize the Telegram Application with timeouts to bypass restrictions
    app = (
        ApplicationBuilder()
        .token(token)
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .build()
    )

    # Route Telegram inputs to the functions inside bot.py
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message_with_search))

    # NEW: Route button clicks to our approval handler
    app.add_handler(CallbackQueryHandler(handle_approval))

    print("System is online! Waiting for Telegram messages...\n" + "-" * 40)

    app.run_polling()


if __name__ == "__main__":
    main()