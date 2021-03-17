import tmdbsimple as tmdb

from stsfy.settings import TMDB_API

tmdb.API_KEY = TMDB_API


def getShowData():
    search = tmdb.Search()
    response = search.movie(query='Superman')

    return search



