from collections import defaultdict
from telegram import Bot, Update
from telegram.error import BadRequest
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, CallbackContext
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps, loads
import os

TOKEN = '2136138549:AAFUlQLFBkh4tB1I6Ifkml9veLvzGjdu6mY'



mongodb_host = os.environ.get('MONGO_HOST', 'mongo')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))



client = MongoClient(mongodb_host, mongodb_port)


db = client['todo']


##логи
##import logging
##logging.basicConfig(format='%(levelname)s - %(message)s', level=logging.DEBUG)
##logger = logging.getLogger(__name__)


def is_bad(text: str) -> bool:
    for word in bad_list:
        if word in text.lower():
            return True
    else:
        return False


def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Вот мои команды:\n/help - список доступных команд,\n/stats - пользователи, упомяновшие о COVID-19', quote=True)


def publish(bot, update):
    str_msg = ' '.join(update.args)
    print("Message from tlg: ", str_msg)


def echo(update: Update, context: CallbackContext) -> None:
    if is_bad(update.message.text):
        chat_id = update.effective_message.chat.title
        user_name = update.effective_message.from_user.name
        if isinstance(chat_id, type(None)):
            chat_id = "Чат-бот/ID " + str(update.effective_message.chat.id)

        a = db[chat_id]
        # print(a)
        if a.find_one({'name': user_name}) is None:
            user_data = {
                "name": user_name,
                "counter": 1,
            }
            a.insert_one(user_data)
        else:
            tmp = a.find_one({'name': user_name})['counter']
            current_name = {'name': user_name}
            current_cnt = {"$set": {'counter': tmp + 1}}
            a.update_one(current_name, current_cnt)

        update.message.reply_text('Данная информация может быть недостоверна', quote=True)


def stats(update: Update, context: CallbackContext) -> None:
    # for i in db.list_collection_names():
    #     print(loads(dumps(db[i].find())))
    #     for k in loads(dumps(db[i].find())):
    #         print('\t\t', k)
    #

    temp = ''
    if update.effective_message.chat.type == 'private':  # private message to bot
        for group in sorted(db.list_collection_names()):
            temp += group + ':\n'
            for d in sorted(loads(dumps(db[group].find())), key=lambda p: (-p['counter'], p['name'])):
                temp += '\U0000221F' + d["name"] + ': ' + str(d["counter"]) + '\n'
            temp += '\n'
    else:
        chat_name = update.effective_message.chat.title
        for d in sorted(loads(dumps(db[chat_name].find())), key=lambda p: (-p['counter'], p['name'])):
            temp += '\U0000221F' + d["name"] + ': ' + str(d["counter"]) + '\n'

    try:
        update.message.reply_text(temp)
    except BadRequest:
        update.message.reply_text("Данных нет")


def track_chats(update: Update, context: CallbackContext) -> None:
    if update.effective_message.left_chat_member['is_bot'] and update.effective_message.left_chat_member['id'] == bot.id:
        chat_name = update.effective_chat.title
        print('Удалена статистика по чату', chat_name)
        db.drop_collection(chat_name)


if __name__ == "__main__":
    with open("key_words.txt", 'r', encoding='utf-8') as f:
        bad_list = f.read().split()

    bot = Bot(token=TOKEN)
    updater = Updater(token=TOKEN, use_context=True)

    publish_handler = CommandHandler('publish', publish)
    help_handler = CommandHandler('help', help)
    stat_handler = CommandHandler('stats', stats)

    updater.dispatcher.add_handler(publish_handler)
    updater.dispatcher.add_handler(help_handler)
    updater.dispatcher.add_handler(stat_handler)

    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    updater.dispatcher.add_handler(MessageHandler(Filters.status_update.left_chat_member, track_chats))

    updater.start_polling()

