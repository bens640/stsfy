import json
from dateutil.parser import *

from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from library.services import *
from stsfy.settings import TMDB_API


def home(request):
    movies = getThisYearMovies()
    tv = getThisYearTv()
    music = getTopAlbums()

    data = {
        "movies": movies,
        'tv': tv,
        'music': music
    }

    return render(request, 'library/home.html', data)


def testPage(request):
    movies = getThisYearMovies()
    tv = getThisYearTv()
    music = getTopAlbums()
    item = getItemDetails(456, '2')

    data = {
        "movies": movies,
        'tv': tv,
        'music': music,
        'item' : item[0]

    }
    for x in request.POST:
        print(x)
    return render(request, 'library/test.html', data)

class TestPage(TemplateView):
    context_object_name = 'data'
    template_name = 'library/test.html'


    # def post(request):

    def get_context_data(self, **kwargs):
        movies = getThisYearMovies()
        tv = getThisYearTv()
        music = getTopAlbums()
        item = getItemDetails(456, '2')

        data = {
            "movies": movies,
            'tv': tv,
            'music': music,
            'item': item[0]

        }
        return data


class SearchResultsView(ListView):
    template_name = 'library/search_results.html'
    context_object_name = 'items'

    def get_queryset(self):

        if self.request.GET.get('q'):
            query = self.request.GET.get('q')
        else:
            query = 'the'

        movies = searchMovies(query)
        tv = searchTv(query)
        artists = musicSearch(query, 'artists')
        albums = musicSearch(query, 'albums')
        context = {
            "movies": movies,
            'tv': tv,
            'artists': artists,
            'albums': albums
        }
        return context


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def detail(request, pk, itemType=1):
    next_air = None
    release_date = None
    item = getItemDetails(pk, itemType)
    if 'next_episode_to_air' in item[0].info() :
        if item[0].info()['next_episode_to_air'] is not None:
            next_air = parse(item[0].info()['next_episode_to_air']['air_date']).strftime('%A'+', %b %d, %Y')
        else:
            next_air = None
    if 'release_date' in item[0].info():
        if item[0].info()['release_date'] is not None:
            release_date = parse(item[0].info()['release_date']).strftime('%A' + ', %b %d, %Y')

    context = {
        "item": item[0],
        'similar': item[1],
        'credits': item[2],
        'airdate': next_air,
        'release' : release_date
    }

    return render(request, 'library/detail.html', context)

def detailMusic(request, pk):

    item = getMusicDetails(pk, '1')
    albums = getMusicDetails(pk, '2')


    context = {
        "item": item,
        'albums': albums
    }

    return render(request, 'library/detail_music.html', context)

def personDetail(request, pk):
    person = getPersonDetail(pk)

    context = {
        'details': person[0],
        'credits': person[1]
    }
    return render(request, 'library/person_detail.html', context)

def tvPage(request):
    context = {
    }
    return render(request, 'library/tv_page.html', context)

def moviePage(request):
    movies = getTopRatedMovies()
    context = {
        'movies': movies
    }
    return render(request, 'library/movie_page.html', context)

def musicPage(request):
    context = {
    }
    return render(request, 'library/music_page.html', context)

def filter(request):
    movies = getThisYearMovies()

    kwargs = {"year": "2021"}
    if request.method == 'POST':
        year = request.POST.get("year_filter", None)
        lang = request.POST.get("lang_filter", None)
        if request.POST.get("year_filter", None):
            kwargs["year"] =  year
        if request.POST.get("lang_filter", None):
            kwargs["language"] = lang
        if request.POST.get("range", None):
            print(request.POST.get("range", None))
    movies = tmdb.Discover().movie(**kwargs)

    data = {
        "movies": movies,
    }



    return render(request, 'library/test.html', data)