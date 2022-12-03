import logging
import time

from telegram.bot import bot, localization
from telegram.keyboards import Keyboards
from telegram.push_msg import push_posts_on_date
from database.methods import update_user, select_data


@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    user_exists = select_data(table="users", column="telegram_id", condition=user_id, condition_column="telegram_id",
                              check_if_exists=True)
    if user_exists ==True:
        pass
    else:
        update_user(user_id=user_id, status=False)
        msg = localization["language"]
        bot.send_message(user_id, msg, reply_markup=Keyboards().choose_language())
        time.sleep(0.5)


@bot.message_handler(commands=["lang"])
def lang(message):
    msg = localization["language"]
    bot.send_message(message.chat.id, msg, reply_markup=Keyboards().choose_language())
    time.sleep(0.5)


@bot.message_handler(commands=["help"])
def lang(message):
    user_id = message.chat.id
    user_lang = select_data(table="users", column="lang", condition=user_id,
                            condition_column="telegram_id", user_settings=True)
    msg = localization[user_lang if user_lang!=None else "EN"]["help"]
    bot.send_message(user_id, msg)
    time.sleep(0.5)


@bot.message_handler(commands=["send_posts"])
def send_posts(message):
    user_id = message.from_user.id
    update_user(user_id=user_id, status=True)
    user_lang = select_data(table="users", column="lang", condition=user_id,
                            condition_column="telegram_id", user_settings=True)
    msg = localization[user_lang if user_lang!=None else "EN"]["send_posts"]
    bot.send_message(message.chat.id, msg)
    time.sleep(0.5)


@bot.message_handler(commands=["stop"])
def stop_posts(message):
    user_id = message.from_user.id
    update_user(user_id=message.from_user.id, status=False)
    user_lang = select_data(table="users", column="lang", condition=user_id,
                            condition_column="telegram_id", user_settings=True)
    msg = localization[user_lang if user_lang!=None else "EN"]["stop_posts"]
    bot.send_message(user_id, msg)
    time.sleep(0.5)


@bot.message_handler(commands=["yesterday_posts"])
def yesterday_posts(message):
    user_id = message.chat.id
    user_lang = select_data(table="users", column="lang", condition=user_id,
                            condition_column="telegram_id", user_settings=True)
    push_posts_on_date(chat_id=user_id, posts_date="y", lang=user_lang if user_lang!=None else "EN")
    time.sleep(0.5)


@bot.message_handler(commands=["today_posts"])
def today_posts(message):
    user_id = message.chat.id
    user_lang = select_data(table="users", column="lang", condition=user_id,
                            condition_column="telegram_id", user_settings=True)
    push_posts_on_date(chat_id=user_id, lang=user_lang if user_lang!=None else "EN")
    time.sleep(0.5)


@bot.callback_query_handler(func=lambda call: ["EN", "BY", "RU"])
def filter_callback(call):
    user_id = call.from_user.id
    update_user(user_id=user_id, lang=call.data)
    user_lang = select_data(table="users", column="lang", condition=user_id,
                            condition_column="telegram_id", user_settings=True)
    msg = localization[user_lang if user_lang!=None else "EN"]["language"]
    bot.send_message(user_id, msg)
    greet_sended = select_data(table="users", column="greet_status", condition=user_id, condition_column="telegram_id",
                               user_settings=True)
    if greet_sended==True:
        pass
    else:
        update_user(user_id=user_id, status=True)
        update_user(user_id=user_id, greet_status=True)
        bot.send_message(user_id, localization[user_lang if user_lang!=None else "EN"]["send_posts"])
    time.sleep(0.5)


@bot.message_handler()
def any_massage(message):
    user_id = message.chat.id
    user_lang = select_data(table="users", column="lang", condition=user_id,
                            condition_column="telegram_id", user_settings=True)
    msg = localization[user_lang if user_lang!=None else "EN"]["fatal_error"]
    bot.send_message(user_id, msg)
    time.sleep(0.5)


while True:
    try:
        bot.polling()
    except Exception as error:
        logging.info(msg=error)
        time.sleep(5)
