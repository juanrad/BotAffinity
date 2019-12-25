from telegram.error import TelegramError, BadRequest


class FilmNotFound(TelegramError):
    pass


class IncorrectSearch(BadRequest):

    def __init__(self, message="Incorrect search"):
        pass
