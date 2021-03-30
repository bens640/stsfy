import tmdbsimple as tmdb
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from stsfy.settings import TMDB_API, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

tmdb.API_KEY = TMDB_API
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                                              client_secret=SPOTIFY_CLIENT_SECRET))


def getTopAlbums():
    sp = spotify.new_releases(country="US")

    return sp['albums']['items']


def musicSearch(q, musicType):
    if musicType == 'artist':
        sp = spotify.search(q='artist:' + q, type='artist')
        return sp['artists']['items']
    else:
        sp = spotify.search(q='album:' + q, type='album')
        return sp['albums']['items']


def getItemDetails(pk, itemType):
    if itemType == '1':
        movie = tmdb.Movies(pk)
        response = movie.info()
        # print(movie)
        return [movie, movie.similar_movies()['results'], movie.credits()['cast']]
    elif itemType == '2':
        tv = tmdb.TV(pk)
        response = tv.info()

        return [tv, tv.similar()['results'], tv.credits()['cast']]


def getMusicDetails(pk, itemType):
    if itemType == '1':
        sp = spotify.artist(pk)
        return sp
    elif itemType == '2':
        sp = spotify.artist_albums(pk)
        # print(sp)
        return sp


def searchMovies(q):
    movies = tmdb.Search()
    response = movies.movie(query=q)
    return movies


def searchTv(q):
    tv = tmdb.Search()
    response = tv.tv(query=q)
    return tv


def getThisYearMovies():
    movies = tmdb.Discover()
    response = movies.movie(year="2021")

    return movies


def getThisYearTv():
    tv = tmdb.Discover()
    response = tv.tv(year="2021")
    # print(response)
    return tv


def getPersonDetail(id):
    person = tmdb.People(id)
    response = person.info()
    credits = tmdb.People(id).combined_credits()

    return [person, credits['cast']]


def getTopRatedMovies():
    kwarg = 'sort_by: popularity.asc'
    movies = tmdb.Discover()
    response = movies.movie()

    return movies


def filterAndSortMovie(*kwargs):
    main_filter = {}
    for filter, value in kwargs:
        main_filter[filter] = value

    return main_filter
