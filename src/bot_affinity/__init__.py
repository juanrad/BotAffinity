# -*- coding: utf-8 -*-
import os
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import logging

from bot_affinity.conversation import pray, bible_quote, HELP_SHARE
from bot_affinity.exception import FilmNotFound, IncorrectSearch

_API_URL = 'https://filmaffinity-unofficial.herokuapp.com/api/'
_API_SEARCH = 'search?'
_API_MOVIE = 'movie/'

_films_cache = []


def _api_film_id(query: str):
    return {'q': query, 'lang': 'EN'}


def _api_film_metadata(film_id: int):
    return requests.get(_API_URL + _API_MOVIE + str(film_id)).json()


def _film_url(id: int):
    return 'https://www.filmaffinity.com/us/film{}.html'.format(str(id))


def _find(query: str, number=5):
    ids_request = requests.get(_API_URL + _API_SEARCH, _api_film_id(query)).json()
    if len(ids_request) < 1:
        raise FilmNotFound('I was unable to find nothing with "{}". Sorry 😭'.format(query))
    n = 1
    global _films_cache
    _films_cache = []
    for id in ids_request:
        if n > number:
            break
        film_id = id['id']
        film_url = _film_url(film_id)
        film_metadata = _api_film_metadata(film_id)
        _films_cache.append({'id': film_id, 'url': film_url, 'metadata': film_metadata})
        n += 1
    return _films_cache


def share(bot_updater, context):
    query = None
    try:
        if len(context.args) < 1:
            raise IncorrectSearch
        query = str.join(' ', context.args)
        _find(query, 5)

        keyboard = []
        n = 1
        for film in _films_cache:
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
        "Hello {}! I'm BotAffinity, I can find Filmaffinty pages for you. Try /find to begin.".format(
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
