# Импортируем необходимые классы.
import sqlite3
import logging
from random import shuffle
from telegram.ext import Application, MessageHandler, filters
from config import BOT_TOKEN
from subjects_update import update_subjects
from telegram.ext import CommandHandler, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InputMediaPhoto

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Определяем функцию-обработчик сообщений.
# У неё два параметра, updater, принявший сообщение и контекст - дополнительная информация о сообщении.
async def play_game3(update, context):
    reply_keyboard = [['/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(
        f"Сейчас мы сыграем в игру 'знаток района'.\n"
        f"В ней вам нужно назвать все вседения о районе."
        f"Чтобы остановить игру, напишите /stop.",
        reply_markup=markup
    )
    return await play_game3_1(update, context)


async def play_game3_1(update, context):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    result = cur.execute("""SELECT name, flag, emblem, center from subjects 
    WHERE id = abs(random() % 82) + 1""").fetchone()
    await update.message.reply_text(
        f'Название района: {result[0]}. Назовите её Административный центр.'
    )
    context.user_data['name'] = result[0]
    context.user_data['flag'] = result[1]
    context.user_data['emblem'] = result[2]
    context.user_data['center'] = result[3]
    context.user_data['right_answers'] = 0
    con.close()
    return 2


async def play_game3_2(update, context):
    center = update.message.text.lower()
    if center == context.user_data.get('center', 'нет').lower():
        await update.message.reply_text(
            f'Вы правы! Продолжим игру...'
        )
        context.user_data['right_answers'] += 1
    else:
        await update.message.reply_text(
            f'Вы ответили неверно. Правильный ответ: {context.user_data.get('center', 'нет')}'
        )
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    result1 = context.user_data.get('flag', 'нет')
    while result1 == context.user_data.get('flag', 'нет'):
        result1 = cur.execute("""SELECT flag from subjects WHERE id = abs(random() % 82) + 1""").fetchone()[0]
    result2 = context.user_data.get('flag', 'нет')
    while result2 == context.user_data.get('flag', 'нет') or result2 == result1:
        result2 = cur.execute("""SELECT flag from subjects WHERE id = abs(random() % 82) + 1""").fetchone()[0]
    image_urls = [
        context.user_data.get('flag', 'нет'),
        result1,
        result2
    ]
    shuffle(image_urls)
    context.user_data['flag_number'] = image_urls.index(context.user_data.get('flag', 'нет')) + 1
    # Создаем медиагруппу
    media_group = [
        InputMediaPhoto(media=url, caption=f'Как вы думаете: какой из этих 3-х флагов принадлежит этому району?\n'
                                           f'В ответ запишите цифру (1-3)' if i == 0 else "")
        for i, url in enumerate(image_urls)
    ]

    await context.bot.send_media_group(
        chat_id=update.effective_chat.id,
        media=media_group
    )
    return 3


async def play_game3_3(update, context):
    flag_number = int(update.message.text)
    if flag_number == context.user_data.get('flag_number', 'нет'):
        await update.message.reply_text(
            f'Вы правы! Продолжим игру...'
        )
        context.user_data['right_answers'] += 1
    else:
        await update.message.reply_text(
            f'Вы ответили неверно. Правильный ответ: {context.user_data.get('flag_number', 'нет')}'
        )
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    result1 = context.user_data.get('emblem', 'нет')
    while result1 == context.user_data.get('emblem', 'нет'):
        result1 = cur.execute("""SELECT emblem from subjects WHERE id = abs(random() % 82) + 1""").fetchone()[0]
    result2 = context.user_data.get('emblem', 'нет')
    while result2 == context.user_data.get('emblem', 'нет') or result2 == result1:
        result2 = cur.execute("""SELECT emblem from subjects WHERE id = abs(random() % 82) + 1""").fetchone()[0]
    image_urls = [
        context.user_data.get('emblem', 'нет'),
        result1,
        result2
    ]
    shuffle(image_urls)
    context.user_data['emblem_number'] = image_urls.index(context.user_data.get('emblem', 'нет')) + 1
    # Создаем медиагруппу
    media_group = [
        InputMediaPhoto(media=url, caption=f'Как вы думаете: какой из этих 3-х гербов принадлежит этому району?\n'
                                           f'В ответ запишите цифру (1-3)' if i == 0 else "")
        for i, url in enumerate(image_urls)
    ]

    await context.bot.send_media_group(
        chat_id=update.effective_chat.id,
        media=media_group
    )
    return 4


async def play_game3_4(update, context):
    emblem_number = int(update.message.text)
    if emblem_number == context.user_data.get('emblem_number', 'нет'):
        await update.message.reply_text(
            f'Вы правы! Продолжим игру...'
        )
        context.user_data['right_answers'] += 1
    else:
        await update.message.reply_text(
            f'Вы ответили неверно. Правильный ответ: {context.user_data.get('emblem_number', 'нет')}'
        )
    await update.message.reply_text(
        f'Итого вы ответили на {context.user_data.get('right_answers', 'нет')} вопросов из 3.'
        f'Давайте начнём следующую игру...'
    )
    return await play_game3_1(update, context)


async def play_game2(update, context):
    reply_keyboard = [['/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(
        f"Сейчас мы сыграем в игру 'угадай регион по флагу'.\n"
        f"Чтобы остановить игру, напишите /stop.",
        reply_markup=markup
    )
    return await play_game2_1(update, context)


async def play_game2_1(update, context):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    result = cur.execute('SELECT name, flag, emblem from subjects WHERE id = abs(random() % 82) + 1').fetchone()
    await context.bot.send_photo(
        update.message.chat_id,
        result[1],
        caption=f"Вот флаг района. Что это за район?"
    )
    context.user_data['emblem'] = result[2]
    context.user_data['name'] = result[0]
    con.close()
    return 2


async def play_game2_2(update, context):
    hint = context.user_data.get('hint', 'нет')
    name = update.message.text.lower().replace('республика', '').replace('край', ''). \
        replace('область', '').replace('АО', '').replace(' ', '')
    if name == context.user_data.get('name', 'нет').lower().replace('республика', '').replace('край', ''). \
            replace('область', '').replace('АО', '').replace(' ', ''):
        await update.message.reply_text(
            f'Вы угадали! Давайте сыграем ещё.',
        )
        context.user_data['hint'] = False
        return await play_game2_1(update, context)
    elif hint is not True:
        await update.message.reply_text(
            f'К сожалению, вы ошиблись. Хотите подсказку?'
        )
        return 3
    else:
        context.user_data['hint'] = False
        await update.message.reply_text(
            f'К сожалению, вы опять ошиблись. Название района: {context.user_data.get('name', 'нет')}.\n'
            f'Давайте сыграем ещё.'
        )
        return await play_game2_1(update, context)


async def play_game2_3(update, context):
    answer = update.message.text
    if 'да' in answer.lower():
        await context.bot.send_photo(
            update.message.chat_id,
            context.user_data.get('emblem', 'нет'),
            caption="Вот герб района. Так что же это за район?"
        )
        context.user_data['hint'] = True
        return 2
    else:
        await update.message.reply_text(
            f'Название района: {context.user_data.get('name', 'нет')}. Давайте сыграем ещё раз.'
        )
        return await play_game2_1(update, context)


async def play_game1(update, context):
    reply_keyboard = [['/stop']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(
        f"Сейчас мы сыграем в игру 'угадай Административный центр по названию республики'.\n"
        f"Чтобы остановить игру, напишите /stop.",
        reply_markup=markup
    )
    return await play_game1_1(update, context)


async def play_game1_1(update, context):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    result = cur.execute('SELECT name, center from subjects WHERE id = abs(random() % 22) + 1').fetchone()
    await update.message.reply_text(
        f'Название республики: {result[0]}. Назовите её Административный центр.'
    )
    context.user_data['center'] = result[1]
    con.close()
    return 2


async def play_game1_2(update, context):
    center = update.message.text
    if center.lower() == context.user_data.get('center', 'нет').lower():
        await update.message.reply_text(
            f'Вы угадали! Давайте сыграем ещё.',
        )
    else:
        await update.message.reply_text(
            f'К сожалению, вы ошиблись. Правильный ответ: {context.user_data.get('center', 'нет')}. '
            f'Давайте сыграем ещё.',
        )
    return await play_game1_1(update, context)


async def get_data1(update, context):
    region = update.message.text
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    try:
        result = cur.execute("""SELECT name, flag, emblem, square, population, center FROM subjects 
        WHERE name = ?""", (region,)).fetchone()
        name, flag, emblem, square, population, center = result
    except:
        reply_keyboard = [['/stop']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
        await update.message.reply_text(
            f'Такого района нет. Попробуйте ещё раз.\n'
            f'Если вы не хотите узнать информацию о районе, напишите /stop',
            reply_markup=markup
        )
        return 1
    await update.message.reply_text(
        f'Название района: {name}\n'
        f'Площадь (км²) района: {square}\n'
        f'({square / 17098246}%)\n'
        f'Численность населения района: {population}\n'
        f'({population / 146119928}%)\n'
        f'Административный центр района: {center}'
    )
    await context.bot.send_photo(
        update.message.chat_id,
        flag,
        caption="Флаг района:"
    )
    await context.bot.send_photo(
        update.message.chat_id,
        emblem,
        caption="Герб района:"
    )
    con.close()
    return ConversationHandler.END


async def get_data(update, context):
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    result = cur.execute('SELECT name from subjects').fetchall()
    result = [f'`{s[0]}`' for s in result]
    await update.message.reply_text(
        f'Выберите район, о котором вы хотите узнать:\n\n{'\n'.join(result)}',
        parse_mode="MarkdownV2"
    )
    con.close()
    return 1


async def data_update(update, context):
    update_subjects()
    await update.message.reply_text(
        f'Данные были успешно обновлены.',
    )


async def start(update, context):
    user = update.effective_user
    reply_keyboard = [['/get_data', '/data_update'],
                      ['/play_game1', '/play_game2', '/play_game3']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_html(
        f"Привет, {user.mention_html()}! Я бот, созданный для того, чтобы запоминать регионы. \n"
        f"Выбери из нижеперечисленных одну команду:\n"
        f"/get_data - выводит все регионы России для того, чтобы вы могли ознакомиться с ними\n"
        f"/data_update - обновляет информацию в базе данных. (Куллдаун команды: 5 минут)\n"
        f"/play_game1 - вы начинаете игру 'угадай Административный центр по названию республики'."
        f"Это самая простая игра из всех.\n"
        f"/play_game2 - вы начинаете игру 'угадай регион по флагу'.\n"
        f"/play_game3 - вы начинаете игру 'знаток региона'.\n"
        f"Чтобы закрыть меню выбора, напишите команду /close.'",
        reply_markup=markup
    )


async def stop(update, context):
    reply_keyboard = [['/start']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    await update.message.reply_text(
        "Процесс успешно завершён.",
        reply_markup=markup
    )
    return ConversationHandler.END


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Меню выбора было успешно закрыто.",
        reply_markup=ReplyKeyboardRemove()
    )


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()
    # Зарегистрируем их в приложении перед
    # регистрацией обработчика текстовых сообщений.
    # Первым параметром конструктора CommandHandler я
    # вляется название команды.
    get_data_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('get_data', get_data)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_data1)],
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    play_game1_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('play_game1', play_game1)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, play_game1_1)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, play_game1_2)],
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    play_game2_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('play_game2', play_game2)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, play_game2_1)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, play_game2_2)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, play_game2_3)],
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    play_game3_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('play_game3', play_game3)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            # Функция читает ответ на первый вопрос и задаёт второй.
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, play_game3_1)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, play_game3_2)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, play_game3_3)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, play_game3_4)],
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(get_data_handler)
    application.add_handler(play_game1_handler)
    application.add_handler(play_game2_handler)
    application.add_handler(play_game3_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", start))
    application.add_handler(CommandHandler("data_update", data_update))
    application.add_handler(CommandHandler("close", close_keyboard))

    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    # text_handler = MessageHandler(filters.TEXT, dialog)

    # Регистрируем обработчик в приложении.
    # application.add_handler(text_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
