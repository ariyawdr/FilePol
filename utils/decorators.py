from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from ..config.settings import settings
from ..database.db_manager import db_manager
from .logger import logger

def admin_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in settings.ADMIN_IDS:
            await update.message.reply_text("شما اجازه دسترسی به این دستور را ندارید.")
            logger.warning(f"Unauthorized admin access attempt by user {user_id} for command {func.__name__}")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def authenticated_user(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user_id = update.effective_user.id
        user = db_manager.get_user_by_telegram_id(user_id)
        if not user or not user.google_drive_refresh_token:
            await update.message.reply_text("لطفاً ابتدا با استفاده از دستور /connect_drive به گوگل درایو متصل شوید.")
            logger.info(f"User {user_id} attempted to use a Google Drive feature without connecting.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def log_errors(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        try:
            return await func(update, context, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in handler {func.__name__} for user {update.effective_user.id}: {e}", exc_info=True)
            if update.message:
                await update.message.reply_text("متاسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید یا با ادمین تماس بگیرید.")
            elif update.callback_query:
                await update.callback_query.answer("متاسفانه خطایی رخ داد.")
            return
    return wrapper

