import os
from telegram.ext import Updater, CommandHandler
import requests

_API_URL = 'https://filmaffinity-unofficial.herokuapp.com/api/'
_API_SEARCH = 'search?'
_API_MOVIE = 'movie/'


def _api_film_id(query: str):
    return {'q': query, 'lang': 'EN'}


def _help_find(bot):
    return bot.message.reply_text(
        "#TODO: HELP WITH FIND".format(bot.message.from_user.first_name))  # TODO


def _film_not_found(bot: str, query: str):
    return bot.message.reply_text(
        'I was unable to find nothing with "{}". Sorry :_('.format(query))


def _print_film_info(bot, film_request: dict, film_url: str):
    description = '''
**Title** : __{}__
**Year** : __{}__
**Duration** : __{}__
**Director** : __{}__
[Filmaffinty]({})
    '''
    description_md = description.format(film_request['title'], str(film_request['year']), str(film_request['duration']),
                                        film_request['director'], film_url)
    bot.message.reply_markdown(description_md)#, disable_notification=True)


def _film_url(id: int):
    return 'https://www.filmaffinity.com/us/film{}.html'.format(str(id))


def find(bot, context):
    if len(context.args) < 1:
        return _help_find(bot)
    query = str.join(' ', context.args)
    id_request = requests.get(_API_URL + _API_SEARCH, _api_film_id(query)).json()
    if len(id_request) < 1:
        return _film_not_found(bot, query)
    film_id = id_request[0]['id']
    film_request = requests.get(_API_URL + _API_MOVIE + str(film_id)).json()
    _print_film_info(bot, film_request, _film_url(film_id))


def helpme(bot):
    bot.message.reply_text(
        "Hello {}! I'm BotAffinity, I can find Filmaffinty pages for you. Try /find to begin.".format(
            bot.message.from_user.first_name))


def bible_quote(bot):
    bot.message.reply_text('https://www.youtube.com/watch?v=P-_A6gqda44')


def pray(bot):
    bot.message.reply_text(
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
    bot = Updater(os.environ['TOKEN'], use_context=True)

    bot.dispatcher.add_handler(CommandHandler('find', find))
    bot.dispatcher.add_handler(CommandHandler('biblequote', bible_quote))
    bot.dispatcher.add_handler(CommandHandler('pray', pray))
    bot.dispatcher.add_handler(CommandHandler('help', helpme))

    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
