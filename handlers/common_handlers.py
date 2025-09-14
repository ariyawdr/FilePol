from telegram import Update
from telegram.ext import ContextTypes
from ..utils.logger import logger

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"سلام {user.mention_html()}!\nبه ربات پُل خوش آمدید. \nاین ربات به شما کمک می‌کند فایل‌های خود را به گوگل درایو آپلود کرده و لینک کوتاه دریافت کنید.\nبرای شروع، از دستور /help استفاده کنید."
    )
    logger.info(f"User {user.id} started the bot.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message when the command /help is issued."""
    help_text = (
        "**دستورات کاربری:**\n"
        "/start - شروع کار با ربات\n"
        "/help - نمایش این راهنما\n"
        "/connect_drive - اتصال به گوگل درایو\n"
        "/setfolder - تنظیم پوشه پیش‌فرض گوگل درایو\n"
        "/setdomain - تنظیم دامنه Short.io\n"
        "/setapikey - تنظیم Short.io API Key\n"
        "\n"
        "**دستورات ادمین (فقط برای ادمین‌ها):**\n"
        "/addadmin <user_id> - افزودن ادمین جدید\n"
        "/removeadmin <user_id> - حذف ادمین\n"
        "/listusers - نمایش لیست کاربران\n"
        "/broadcast <message> - ارسال پیام همگانی\n"
        "\n"
        "**آپلود فایل:**\n"
        "برای آپلود فایل، کافیست فایل خود را برای ربات ارسال کنید."
    )
    await update.message.reply_text(help_text, parse_mode=\"Markdown\")
    logger.info(f"User {update.effective_user.id} requested help.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a message to the user."""
    logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)
    if update.effective_message:
        await update.effective_message.reply_text(
            "متاسفانه خطایی در پردازش درخواست شما رخ داد. لطفاً دوباره تلاش کنید."
        )


