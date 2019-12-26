# -*- coding: utf-8 -*-
import os
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

from bot_affinity.conversation import pray, bible_quote, HELP_SHARE
from bot_affinity.exception import FilmNotFound, IncorrectSearch
from bot_affinity.filmaffinity_api import find_film

_films_cache = []


def share(bot_updater, context):
    query = None
    global _films_cache
    _films_cache = []
    try:
        if len(context.args) < 1:
            raise IncorrectSearch
        query = str.join(' ', context.args)
        films = find_film(query, _films_cache, 5)

        keyboard = []
        n = 1
        for film in films:
            button = InlineKeyboardButton(
                '{} ({}) from {}'.format(film['metadata']['title'], film['metadata']['year'],
                                         film['metadata']['director']),
                callback_data=str(n))
            keyboard.append([button])
            n += 1

        reply_markup = InlineKeyboardMarkup(keyboard)
        bot_updater.message.reply_text('Nice! Please choose the movie you want to share:', reply_markup=reply_markup)

    except FilmNotFound as e:
        bot_updater.message.reply_text(e.message)
    except IncorrectSearch:
        return bot_updater.message.reply_text(HELP_SHARE)


def helpme(bot_updater, context):
    bot_updater.message.reply_text(
        "Hello {}! I'm BotAffinity, I can find Filmaffinty pages for you." +
        " Try /film or /share followed by any movie name to begin.".format(
            bot_updater.message.from_user.first_name))


def choose_film_button(bot_updater, context):
    query = bot_updater.callback_query
    film_index = int(query.data) - 1
    film = _films_cache[film_index]
    user = bot_updater.effective_user
    query.edit_message_text(text="{} recomends {} ".format(user.first_name, film['url']))


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    bot_updater = Updater(os.environ['TOKEN'], use_context=True, workers=1)

    dispatcher = bot_updater.dispatcher

    dispatcher.add_handler(CommandHandler('share', share))
    dispatcher.add_handler(CommandHandler('film', share))
    dispatcher.add_handler(CallbackQueryHandler(choose_film_button))
    dispatcher.add_handler(CommandHandler('biblequote', bible_quote))
    dispatcher.add_handler(CommandHandler('pray', pray))
    dispatcher.add_handler(CommandHandler('help', helpme))

    bot_updater.start_polling()
    bot_updater.idle()


if __name__ == '__main__':
    main()
