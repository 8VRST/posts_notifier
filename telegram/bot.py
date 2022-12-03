import telebot

from utils.json_pocessing import open_json_file


creds = open_json_file("telegram/creds.json")


localization = open_json_file("telegram/localization.json")


bot = telebot.TeleBot(creds["token"])