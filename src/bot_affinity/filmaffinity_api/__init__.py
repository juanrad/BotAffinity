# -*- coding: utf-8 -*-
import os
import requests

from bot_affinity.exception import FilmNotFound, IncorrectSearch

_API_URL = 'https://filmaffinity-unofficial.herokuapp.com/api/'
_API_SEARCH = 'search?'
_API_MOVIE = 'movie/'


def _api_film_id(query: str):
    return {'q': query, 'lang': 'EN'}


def _api_film_metadata(film_id: int):
    return requests.get(_API_URL + _API_MOVIE + str(film_id)).json()


def _film_url(id: int):
    return 'https://www.filmaffinity.com/us/film{}.html'.format(str(id))


def find_film(query: str, films, number=5):
    ids_request = requests.get(_API_URL + _API_SEARCH, _api_film_id(query)).json()
    if len(ids_request) < 1:
        raise FilmNotFound('I was unable to find nothing with "{}". Sorry 😭'.format(query))
    n = 1
    for id in ids_request:
        if n > number:
            break
        film_id = id['id']
        film_url = _film_url(film_id)
        film_metadata = _api_film_metadata(film_id)
        films.append({'id': film_id, 'url': film_url, 'metadata': film_metadata})
        n += 1
    return films
