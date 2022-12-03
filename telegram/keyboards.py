from telebot import types


class Keyboards:

    def __init__(self):
        self.inline_markup = types.InlineKeyboardMarkup()

    def choose_language(self):
        languages = [
            types.InlineKeyboardButton("EN", callback_data="EN"),
            types.InlineKeyboardButton("BY", callback_data="BY"),
            types.InlineKeyboardButton("RU", callback_data="RU")
        ]
        self.inline_markup.add(*languages)
        return self.inline_markup