from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
from ..database.db_manager import db_manager
from ..utils.decorators import log_errors, authenticated_user
from ..utils.logger import logger
from ..utils.google_auth_flow import google_auth_flow
from ..services.google_drive_service import google_drive_service
from ..services.shortio_service import shortio_service
import os

# States for ConversationHandler
CONNECT_DRIVE_CODE, SET_FOLDER_NAME, SET_SHORTIO_DOMAIN, SET_SHORTIO_API_KEY = range(4)

@log_errors
async def connect_drive_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the Google Drive connection flow."""
    user_id = update.effective_user.id
    user = db_manager.get_or_create_user(user_id)

    if user.google_drive_refresh_token:
        await update.message.reply_text("شما قبلاً به گوگل درایو متصل شده‌اید. برای اتصال مجدد، ابتدا باید اتصال قبلی را قطع کنید (این قابلیت هنوز پیاده‌سازی نشده است).")
        return ConversationHandler.END

    authorization_url, flow = google_auth_flow.get_authorization_url(state=str(user_id))
    context.user_data["google_auth_flow"] = flow

    await update.message.reply_text(
        f"برای اتصال به گوگل درایو، لطفاً روی لینک زیر کلیک کنید، دسترسی‌ها را تأیید کنید و کد دریافتی را اینجا برای من ارسال کنید:\n\n{authorization_url}"
    )
    logger.info(f"User {user_id} initiated Google Drive connection. Auth URL generated.")
    return CONNECT_DRIVE_CODE

@log_errors
async def connect_drive_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Exchanges the authorization code for a refresh token."""
    user_id = update.effective_user.id
    auth_code = update.message.text.strip()
    flow = context.user_data.get("google_auth_flow")

    if not flow:
        await update.message.reply_text("خطا: جریان احراز هویت یافت نشد. لطفاً دوباره /connect_drive را شروع کنید.")
        logger.error(f"User {user_id} provided code but no auth flow in context.")
        return ConversationHandler.END

    try:
        refresh_token = google_auth_flow.exchange_code_for_token(auth_code, flow)
        user = db_manager.get_user_by_telegram_id(user_id)
        user.google_drive_refresh_token = refresh_token
        db_manager.update_user(user)

        await update.message.reply_text("با موفقیت به گوگل درایو متصل شدید!\nاکنون می‌توانید با دستور /setfolder پوشه پیش‌فرض آپلود را تنظیم کنید.")
        logger.info(f"User {user_id} successfully connected to Google Drive.")
    except Exception as e:
        await update.message.reply_text(f"خطا در اتصال به گوگل درایو: {e}\nلطفاً کد را بررسی کرده و دوباره تلاش کنید.")
        logger.error(f"User {user_id} failed to connect to Google Drive: {e}", exc_info=True)
    finally:
        if "google_auth_flow" in context.user_data:
            del context.user_data["google_auth_flow"]
    
    return ConversationHandler.END

@log_errors
async def set_folder_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation to set the Google Drive folder."""
    user_id = update.effective_user.id
    user = db_manager.get_user_by_telegram_id(user_id)

    if not user or not user.google_drive_refresh_token:
        await update.message.reply_text("لطفاً ابتدا با استفاده از دستور /connect_drive به گوگل درایو متصل شوید.")
        return ConversationHandler.END

    await update.message.reply_text("لطفاً نام پوشه‌ای که می‌خواهید فایل‌ها در آن آپلود شوند را وارد کنید. اگر پوشه وجود نداشته باشد، ایجاد خواهد شد.")
    logger.info(f"User {user_id} initiated setting Google Drive folder.")
    return SET_FOLDER_NAME

@log_errors
async def set_folder_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sets the Google Drive folder name and finds/creates it."""
    user_id = update.effective_user.id
    folder_name = update.message.text.strip()
    user = db_manager.get_user_by_telegram_id(user_id)

    if not user or not user.google_drive_refresh_token:
        await update.message.reply_text("خطا: اتصال گوگل درایو یافت نشد. لطفاً دوباره /connect_drive را شروع کنید.")
        logger.error(f"User {user_id} provided folder name but no refresh token.")
        return ConversationHandler.END

    try:
        folder_id = google_drive_service.find_or_create_folder(user.google_drive_refresh_token, folder_name)
        user.google_drive_folder_id = folder_id
        db_manager.update_user(user)
        await update.message.reply_text(f"پوشه پیش‌فرض گوگل درایو با نام \`{folder_name}\` با موفقیت تنظیم شد.", parse_mode=\"Markdown\")
        logger.info(f"User {user_id} set Google Drive folder to {folder_name} ({folder_id}).")
    except Exception as e:
        await update.message.reply_text(f"خطا در تنظیم پوشه گوگل درایو: {e}\nلطفاً دوباره تلاش کنید.")
        logger.error(f"User {user_id} failed to set Google Drive folder: {e}", exc_info=True)
    
    return ConversationHandler.END

@log_errors
async def set_shortio_domain_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation to set the Short.io domain."""
    user_id = update.effective_user.id
    await update.message.reply_text("لطفاً دامنه Short.io خود را وارد کنید (مثال: `my.short.io`).")
    logger.info(f"User {user_id} initiated setting Short.io domain.")
    return SET_SHORTIO_DOMAIN

@log_errors
async def set_shortio_domain_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sets the Short.io domain name."""
    user_id = update.effective_user.id
    domain = update.message.text.strip()
    user = db_manager.get_user_by_telegram_id(user_id)
    user.shortio_domain = domain
    db_manager.update_user(user)
    await update.message.reply_text(f"دامنه Short.io با موفقیت به \`{domain}\` تنظیم شد.", parse_mode=\"Markdown\")
    logger.info(f"User {user_id} set Short.io domain to {domain}.")
    return ConversationHandler.END

@log_errors
async def set_shortio_api_key_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation to set the Short.io API Key."""
    user_id = update.effective_user.id
    await update.message.reply_text("لطفاً Short.io API Key خود را وارد کنید.")
    logger.info(f"User {user_id} initiated setting Short.io API Key.")
    return SET_SHORTIO_API_KEY

@log_errors
async def set_shortio_api_key_value(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sets the Short.io API Key."""
    user_id = update.effective_user.id
    api_key = update.message.text.strip()
    user = db_manager.get_user_by_telegram_id(user_id)
    user.shortio_api_key = api_key
    db_manager.update_user(user)
    await update.message.reply_text("Short.io API Key با موفقیت تنظیم شد.")
    logger.info(f"User {user_id} set Short.io API Key.")
    return ConversationHandler.END

@authenticated_user
@log_errors
async def handle_document_upload(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles document uploads, uploads to Google Drive, and shortens the link."""
    user_id = update.effective_user.id
    user = db_manager.get_user_by_telegram_id(user_id)

    if not user.google_drive_folder_id:
        await update.message.reply_text("لطفاً ابتدا با دستور /setfolder پوشه پیش‌فرض گوگل درایو را تنظیم کنید.")
        return
    
    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    telegram_file = await context.bot.get_file(file_id)

    # Download the file temporarily
    download_path = f"/tmp/{file_name}"
    await telegram_file.download_to_drive(download_path)
    logger.info(f"User {user_id} downloaded file {file_name} to {download_path}.")

    try:
        # Upload to Google Drive
        await update.message.reply_text(f"در حال آپلود فایل \`{file_name}\` به گوگل درایو...")
        drive_link = google_drive_service.upload_file(user.google_drive_refresh_token, download_path, user.google_drive_folder_id)
        
        if drive_link:
            await update.message.reply_text(f"فایل با موفقیت آپلود شد! لینک گوگل درایو: {drive_link}")
            logger.info(f"User {user_id} uploaded {file_name} to Google Drive. Link: {drive_link}")

            # Shorten link if Short.io is configured
            if user.shortio_api_key and user.shortio_domain:
                await update.message.reply_text("در حال کوتاه کردن لینک با Short.io...")
                short_link = shortio_service.shorten_link(drive_link, user.shortio_domain)
                if short_link:
                    await update.message.reply_text(f"لینک کوتاه شده: {short_link}")
                    logger.info(f"User {user_id} shortened link to {short_link}.")
                else:
                    await update.message.reply_text("خطا در کوتاه کردن لینک با Short.io.")
            elif user.shortio_api_key or user.shortio_domain:
                await update.message.reply_text("برای کوتاه کردن لینک، هم API Key و هم دامنه Short.io باید تنظیم شده باشند.")
        else:
            await update.message.reply_text("خطا در آپلود فایل به گوگل درایو.")

    except Exception as e:
        await update.message.reply_text(f"خطا در پردازش فایل: {e}")
        logger.error(f"Error processing file for user {user_id}: {e}", exc_info=True)
    finally:
        # Clean up the downloaded file
        if os.path.exists(download_path):
            os.remove(download_path)
            logger.info(f"Cleaned up temporary file: {download_path}")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text("عملیات لغو شد.")
    logger.info(f"User {update.effective_user.id} cancelled a conversation.")
    return ConversationHandler.END

def setup_user_handlers(application):
    # Conversation handler for /connect_drive
    connect_drive_handler = ConversationHandler(
        entry_points=[CommandHandler("connect_drive", connect_drive_start)],
        states={
            CONNECT_DRIVE_CODE: [MessageHandler(filters.TEXT & ~filters.COMMAND, connect_drive_code)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(connect_drive_handler)

    # Conversation handler for /setfolder
    set_folder_handler = ConversationHandler(
        entry_points=[CommandHandler("setfolder", set_folder_start)],
        states={
            SET_FOLDER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_folder_name)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(set_folder_handler)

    # Conversation handler for /setdomain
    set_shortio_domain_handler = ConversationHandler(
        entry_points=[CommandHandler("setdomain", set_shortio_domain_start)],
        states={
            SET_SHORTIO_DOMAIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_shortio_domain_name)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(set_shortio_domain_handler)

    # Conversation handler for /setapikey
    set_shortio_api_key_handler = ConversationHandler(
        entry_points=[CommandHandler("setapikey", set_shortio_api_key_start)],
        states={
            SET_SHORTIO_API_KEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_shortio_api_key_value)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(set_shortio_api_key_handler)

    # Handler for document uploads
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document_upload))

    logger.info("User handlers set up.")

