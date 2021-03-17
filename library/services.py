import tmdbsimple as tmdb

from stsfy.settings import TMDB_API

tmdb.API_KEY = TMDB_API


def getShowData():
    movie = tmdb.Movies(603)
    response = movie.info()
    print(movie.title)
    return movie



