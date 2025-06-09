# main.py

import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# --- Ваші налаштування ---
TELEGRAM_BOT_TOKEN = "7888461204:AAEf1X2YtlV4-DMc6A5LQuQAqMU7bTJ4Tdg"
ADMIN_USER_IDS = [797316319]
# ---------------------------

# URL вашого Flask-сервера
REPORT_PAGE_URL = "http://localhost:5000/report"

# Налаштування логування
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/start — надсилаємо посилання на веб-форму."""
    user = update.effective_user
    welcome_message = (
        "Вітаю! Якщо ви хочете написати нам повідомлення, перейдіть за цим посиланням:\n\n"
        f"{REPORT_PAGE_URL}\n\n"
        "Тут ви зможете зашифрувати і відправити текст, і він надійде напряму адміністраторам."
    )
    await update.message.reply_text(welcome_message)
    logger.info(f"User {user.id} opened /start, sent link to web-form.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/help — теж просто даємо лінк на веб-форму."""
    help_text = (
        "Щоб надіслати нам повідомлення, скористайтеся нашою веб-формою:\n\n"
        f"{REPORT_PAGE_URL}\n\n"
        "Повідомлення буде зашифроване у вашому браузері, а потім доставлене адміністраторам."
    )
    await update.message.reply_text(help_text)


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Усі інші повідомлення/команди → знову відсилаємо лінк на форму.
    Щоб нічого не залишалося в чаті.
    """
    info = (
        "Ви можете залишити нам повідомлення лише через веб-форму, щоб історія не залишалася в чаті:\n\n"
        f"{REPORT_PAGE_URL}"
    )
    await update.message.reply_text(info)


def main() -> None:
    if TELEGRAM_BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        logger.error("Будь ласка, встановіть TELEGRAM_BOT_TOKEN у main.py")
        return

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Усе інше (text чи commands) — перекидаємо на форму
    application.add_handler(
        MessageHandler(filters.TEXT | filters.COMMAND, unknown_command)
    )

    logger.info("Bot starting...")
    application.run_polling()


if __name__ == "__main__":
    main()