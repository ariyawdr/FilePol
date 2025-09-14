from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from ..database.db_manager import db_manager
from ..config.settings import settings
from ..utils.decorators import admin_only, log_errors
from ..utils.logger import logger

@admin_only
@log_errors
async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Adds a new admin by user ID."""
    if not context.args:
        await update.message.reply_text("لطفاً یک User ID برای افزودن ادمین وارد کنید. مثال: `/addadmin 123456789`")
        return
    
    try:
        new_admin_id = int(context.args[0])
        user = db_manager.get_or_create_user(new_admin_id)
        if user.is_admin:
            await update.message.reply_text(f"کاربر {new_admin_id} از قبل ادمین است.")
            return
        
        user.is_admin = True
        db_manager.update_user(user)
        settings.ADMIN_IDS.append(new_admin_id) # Update in-memory settings
        await update.message.reply_text(f"کاربر {new_admin_id} با موفقیت به عنوان ادمین اضافه شد.")
        logger.info(f"Admin {update.effective_user.id} added new admin: {new_admin_id}")
    except ValueError:
        await update.message.reply_text("User ID نامعتبر است. لطفاً یک عدد وارد کنید.")
    except Exception as e:
        logger.error(f"Error adding admin: {e}", exc_info=True)
        await update.message.reply_text("خطا در افزودن ادمین.")

@admin_only
@log_errors
async def remove_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Removes an admin by user ID."""
    if not context.args:
        await update.message.reply_text("لطفاً یک User ID برای حذف ادمین وارد کنید. مثال: `/removeadmin 123456789`")
        return
    
    try:
        admin_to_remove_id = int(context.args[0])
        if admin_to_remove_id == update.effective_user.id:
            await update.message.reply_text("شما نمی‌توانید خودتان را از لیست ادمین‌ها حذف کنید.")
            return

        user = db_manager.get_user_by_telegram_id(admin_to_remove_id)
        if not user or not user.is_admin:
            await update.message.reply_text(f"کاربر {admin_to_remove_id} ادمین نیست.")
            return
        
        user.is_admin = False
        db_manager.update_user(user)
        if admin_to_remove_id in settings.ADMIN_IDS:
            settings.ADMIN_IDS.remove(admin_to_remove_id) # Update in-memory settings
        await update.message.reply_text(f"کاربر {admin_to_remove_id} با موفقیت از لیست ادمین‌ها حذف شد.")
        logger.info(f"Admin {update.effective_user.id} removed admin: {admin_to_remove_id}")
    except ValueError:
        await update.message.reply_text("User ID نامعتبر است. لطفاً یک عدد وارد کنید.")
    except Exception as e:
        logger.error(f"Error removing admin: {e}", exc_info=True)
        await update.message.reply_text("خطا در حذف ادمین.")

@admin_only
@log_errors
async def list_users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lists all registered users and their admin status."""
    session = db_manager.get_session()
    users = session.query(db_manager.User).all()
    session.close()

    if not users:
        await update.message.reply_text("هیچ کاربری در دیتابیس ثبت نشده است.")
        return

    user_list_text = "**لیست کاربران:**\n"
    for user in users:
        status = "ادمین" if user.is_admin else "کاربر عادی"
        user_list_text += f"- ID: `{user.telegram_id}` | وضعیت: {status}\n"
    
    await update.message.reply_text(user_list_text, parse_mode=\"Markdown\")
    logger.info(f"Admin {update.effective_user.id} requested user list.")

@admin_only
@log_errors
async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a broadcast message to all users."""
    if not context.args:
        await update.message.reply_text("لطفاً پیامی برای ارسال همگانی وارد کنید. مثال: `/broadcast سلام به همه!`")
        return
    
    message_to_send = " ".join(context.args)
    session = db_manager.get_session()
    users = session.query(db_manager.User).all()
    session.close()

    sent_count = 0
    for user in users:
        try:
            await context.bot.send_message(chat_id=user.telegram_id, text=message_to_send)
            sent_count += 1
        except Exception as e:
            logger.warning(f"Could not send broadcast message to user {user.telegram_id}: {e}")
    
    await update.message.reply_text(f"پیام همگانی به {sent_count} کاربر ارسال شد.")
    logger.info(f"Admin {update.effective_user.id} sent broadcast message to {sent_count} users.")

def setup_admin_handlers(application):
    application.add_handler(CommandHandler("addadmin", add_admin))
    application.add_handler(CommandHandler("removeadmin", remove_admin))
    application.add_handler(CommandHandler("listusers", list_users))
    application.add_handler(CommandHandler("broadcast", broadcast_message))

