import tmdbsimple as tmdb
import spotipy
from django.contrib import messages
from spotipy.oauth2 import SpotifyClientCredentials

from library.models import UserItem, Item
from stsfy.settings import TMDB_API, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from dateutil.parser import *

from users.models import Membership

tmdb.API_KEY = TMDB_API
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                                              client_secret=SPOTIFY_CLIENT_SECRET))


def getTopAlbums():
    sp = spotify.new_releases(country="US")
    # print(sp)
    return sp['albums']['items']


def musicSearch(q, musicType):
    if musicType == 'artists':
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
    elif itemType == '3':
        sp = spotify.album(pk)

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


def getGenres(type):
    if type == 'movie':
        g = tmdb.Genres()
        response = g.movie_list()
        return response.items()
    elif type == 'tv':
        g = tmdb.Genres()
        response = g.tv_list()
        return response.items()


def getUserItem(request, item):
    current_item = Item.objects.filter(item_id=item.id).first()

    if request.user.is_authenticated:
        user_groups = Membership.objects.filter(person=request.user)
        user_has_item = UserItem.objects.filter(item=current_item).filter(owned_by=request.user)

    else:
        user_groups = []
        user_has_item = []
    return [current_item, user_has_item, user_groups]


def add_item(request, item, item_type):
    item_info = getUserItem(request, item)

    if item_type == '1':
        print('movie')
    elif item_type == '2':

        if item_info[1]:
            print('exists?')
            messages.success(request, item.name + ' is already in your watchlist')
        elif Item.objects.filter(item_id=item.id).exists():
            s1 = Item.objects.get(item_id=item.id)
            ss = UserItem(item=s1, owned_by=request.user)
            ss.save()
            messages.success(request, item.name + ' has been added')
        else:
            s = Item(owned_by=request.user, item_id=item.id, name=item.name)
            s.save()
            ss = UserItem(item=s, owned_by=request.user)
            ss.save()
            messages.success(request, item.name + ' has been added')
            print("Created and saved")
    return item_info

def remove_item(request, item):
    current_item = Item.objects.filter(item_id=item.id).first()
    item = UserItem.objects.filter(item=current_item, owned_by=request.user)
    item.delete()
    messages.warning(request, 'This show has been removed from your watchlist')