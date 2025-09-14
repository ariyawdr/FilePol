import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from config.settings import settings
from database.db_manager import db_manager
from utils.logger import logger

# Import handlers (will be created in subsequent steps)
from handlers.admin_handlers import setup_admin_handlers
from handlers.user_handlers import setup_user_handlers
from handlers.common_handlers import start, help_command, error_handler

def main():
    logger.info("Starting bot initialization...")

    # Create the Application and pass your bot's token.
    application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()

    # Register common handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Register admin handlers
    setup_admin_handlers(application)

    # Register user handlers
    setup_user_handlers(application)

    # Register error handler
    application.add_error_handler(error_handler)

    logger.info("Bot initialization complete. Polling for updates...")
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

