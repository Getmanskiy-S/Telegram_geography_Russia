from telegram import Update
from config import BOT_TOKEN
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters
)

# Состояния диалога


async def get_data(update, context):
    await update.message.reply_text("Введите параметр X:")
    return 1  # Активируем состояние


async def get_data1(update, context):
    user_input = update.message.text
    await update.message.reply_text(f"Вы ввели: {user_input}. Введите параметр Y:")
    return 1  # Можно изменить состояние или завершить диалог


async def stop(update, context):
    await update.message.reply_text("Диалог остановлен.")
    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('get_data', get_data)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_data1)],
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
