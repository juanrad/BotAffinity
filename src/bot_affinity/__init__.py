import os
from telegram.ext import Updater, CommandHandler


def helpme(update, context):
    update.message.reply_text(
        "Hello {}! I'm BotAffinity, I can find Filmaffinty pages for you. Try /find to begin.".format(
            update.message.from_user.first_name))

def bible_quote(update,context):
    update.message.reply_text('https://www.youtube.com/watch?v=P-_A6gqda44')

def pray(update, context):
    update.message.reply_text(
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


updater = Updater(os.environ['TOKEN'], use_context=True)

updater.dispatcher.add_handler(CommandHandler('biblequote', bible_quote))
updater.dispatcher.add_handler(CommandHandler('pray', pray))
updater.dispatcher.add_handler(CommandHandler('help', helpme))

updater.start_polling()
updater.idle()
