import logging
from datetime import date, timedelta

from telegram.bot import bot, creds, localization
from database.methods import select_data


def push_posts(user, posts):
    try:
        for post in posts:
            bot.send_message(user, post)
    except Exception as error:
        try:
            logging.error(msg=str(error))
            bot.send_message(creds["admin_id"], "ERROR while push_posts --->>> " + str(error))
        except Exception as error:
            logging.info(msg=error)


def push_posts_on_date(chat_id, lang, posts_date=None):
    try:
        d_min = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d") if posts_date=="y" else date.today().strftime("%Y-%m-%d")
        d_max = date.today().strftime("%Y-%m-%d") if posts_date=="y" else (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        msg_date = (date.today() - timedelta(days=1)).strftime("%d.%m.%Y") if posts_date=="y" else date.today().strftime("%d.%m.%Y")
        posts = select_data(table="links", column="link", by_timestamp=True, date_min=d_min, date_max=d_max)
        msg = localization[lang]["yesterday_posts"].format(len(posts), msg_date) if posts_date=="y" else localization[lang]["today_posts"].format(len(posts))
        for post in posts:
            bot.send_message(chat_id, post)
        bot.send_message(chat_id, msg)
    except Exception as error:
        try:
            logging.error(msg=str(error))
            bot.send_message(creds["admin_id"], "ERROR while push_posts_on_date --->>> " + str(error))
        except Exception as error:
            logging.info(msg=error)