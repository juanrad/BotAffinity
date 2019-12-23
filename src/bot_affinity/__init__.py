import os
from telegram.ext import Updater, CommandHandler
import requests
import logging

_API_URL = 'https://filmaffinity-unofficial.herokuapp.com/api/'
_API_SEARCH = 'search?'
_API_MOVIE = 'movie/'


def _api_film_id(query: str):
    return {'q': query, 'lang': 'EN'}


def _api_film_metadata(film_id: int):
    return requests.get(_API_URL + _API_MOVIE + str(film_id)).json()


def _help_find(bot_updater):
    return bot_updater.message.reply_text(
        "#TODO: HELP WITH FIND".format(bot_updater.message.from_user.first_name))  # TODO


def _film_not_found(bot_updater, query: str):
    return bot_updater.message.reply_text(
        'I was unable to find nothing with "{}". Sorry :_('.format(query))


def _film_url(id: int):
    return 'https://www.filmaffinity.com/us/film{}.html'.format(str(id))


def _find(bot_updater, context):
    if len(context.args) < 1:
        return _help_find(bot_updater)
    query = str.join(' ', context.args)
    id_request = requests.get(_API_URL + _API_SEARCH, _api_film_id(query)).json()
    if len(id_request) < 1:
        return _film_not_found(bot_updater, query)
    film_id = id_request[0]['id']
    film_url = _film_url(film_id)
    film_metadata = _api_film_metadata(film_id)
    return {'id': film_id, 'url': film_url, 'metadata': film_metadata}


def share(bot_updater, context):
    film = _find(bot_updater, context)
    user = bot_updater.message.from_user
    bot_updater.message.reply_text("{} recomends {} ".format(user.first_name, film['url']))


def helpme(bot_updater, context):
    bot_updater.message.reply_text(
        "Hello {}! I'm BotAffinity, I can find Filmaffinty pages for you. Try /find to begin.".format(
            bot_updater.message.from_user.first_name))


def bible_quote(bot_updater, context):
    bot_updater.message.reply_text('https://www.youtube.com/watch?v=P-_A6gqda44')


def pray(bot_updater, context):
    bot_updater.message.reply_text(
        """
This is my rifle. There are many like it, but this one is mine.
My rifle is my best friend. It is my life. 
I must master it as I must master my life.
Without me, my rifle is useless. 
Without my rifle, I am useless. 
I must fire my rifle true. 
I must shoot straighter than my enemy who is trying to kill me. 
I must shoot him before he shoots me. I will ... 
Before God, I swear this creed. 
My rifle and myself are the defenders of my country. 
We are the masters of our enemy. 
We are the saviors of my life.
So be it, until there is no enemy, but peace. 

Amen.
"""
    )


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    bot_updater = Updater(os.environ['TOKEN'], use_context=True, workers=1)

    dispatcher = bot_updater.dispatcher

    dispatcher.add_handler(CommandHandler('share', share))
    dispatcher.add_handler(CommandHandler('biblequote', bible_quote))
    dispatcher.add_handler(CommandHandler('pray', pray))
    dispatcher.add_handler(CommandHandler('help', helpme))

    bot_updater.start_polling()
    bot_updater.idle()


if __name__ == '__main__':
    main()
