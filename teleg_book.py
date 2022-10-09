from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from random import randint
from config import TOKEN
import csv

CHOICE, FIO, SEARCH, SEARCH_DELETE, TEL = range(5)


def start(update, context):
    update.message.reply_text(
        'Шалом! Я (кажется) умею работать со справочником. Что сделаем? \n'
        'Команда /stop, чтобы завершить базар.\n\n')
    update.message.reply_text(
        '1 - добавить человека \n2 - найти человека\n'
        '3 - обновить данные записи \n4 - удалить запись'
    )
    return CHOICE


def choice(update, context):
    user_choice = update.message.text
    if user_choice == '1':
        update.message.reply_text('Фамилия Имя:')
        return FIO
    if user_choice == '2':
        context.bot.send_message(
            update.effective_chat.id, 'Введите значение для поиска: '
        )
        return SEARCH

    if user_choice == '3':
        text = read_csv()
        context.bot.send_message(
            update.effective_chat.id, text)
        return start(update, context)

    if user_choice == '4':
        context.bot.send_message(
            update.effective_chat.id, 'Введите значение для удаления: ')
        return SEARCH_DELETE

    else:
        update.message.reply_text(
            'Может всё-таки выберешь из предложенного?')


def fio(update, context):
    lst = []
    text = update.message.text
    lst.append(text)
    update.message.reply_text(
        'Номер телефона: ')
    with open('database.csv', mode='w', encoding='utf-8-sig') as w_file:
        file_writer = csv.writer(w_file, delimiter=',', lineterminator=',')
        file_writer.writerow(lst)
    return TEL


def search(update, context):
    get_info = update.message.text
    with open('database.csv', mode='r', encoding='utf-8-sig') as r_file:
        reader = csv.reader(r_file)
        for i in reader:
            if get_info in i:
                return i


def search_delete(update, context):
    get_info = update.message.text
    with open('database.csv', mode='w', encoding='utf-8-sig') as w_file:
        writer = csv.writer(w_file)
        for i in writer:
            if get_info in i:
                writer.remove(i)


def tel(update, context):
    get_info = update.message.text
    with open('database.csv', mode='w', encoding='utf-8-sig') as w_file:
        writer = csv.writer(w_file)
        for i in writer:
            if get_info in i:
                i = input('Вводи новые данные через , без пробелов')


def stop(update, context):
    update.message.reply_text(
        'Ну и ладно, не больно-то и хотелось.\n'
        'Если передумаешь, ты знаешь, где меня найти'
    )
    return ConversationHandler.END


bot_token = TOKEN
bot = Bot(bot_token)
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher
conversation_handler = ConversationHandler(entry_points=[CommandHandler('start', start)],
                                           states={
    CHOICE: [MessageHandler(Filters.text & ~Filters.command, choice)],
    FIO: [MessageHandler(Filters.text & ~Filters.command, fio)],
    SEARCH: [MessageHandler(Filters.text & ~Filters.command, search)],
    SEARCH_DELETE: [MessageHandler(Filters.text & ~Filters.command, search_delete)],
    TEL: [MessageHandler(Filters.text & ~Filters.command, tel)]
},
    fallbacks=[CommandHandler('stop', stop)]
)

dispatcher.add_handler(conversation_handler)

updater.start_polling()
updater.idle()
