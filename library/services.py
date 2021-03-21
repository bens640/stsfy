import tmdbsimple as tmdb
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from stsfy.settings import TMDB_API, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

tmdb.API_KEY = TMDB_API
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,client_secret=SPOTIFY_CLIENT_SECRET))


def getTopAlbums():
    sp = spotify.new_releases(country="US")
    return sp['albums']['items']

def musicSearch(q, type):
    if type == 'artist':
        sp = spotify.search(q='artist:' + q, type='artist')
        return sp['artists']['items']
    else:
        sp = spotify.search(q='album:' + q, type='album')
        return sp['albums']['items']



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

    return tv

