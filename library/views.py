import json

from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

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

    data = {
        "movies": movies,
        'tv': tv,
        'music': music,

    }

    return render(request, 'library/test.html', data)


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


def add(request):
    val1 = request.POST.get('num1', None)


    return render(request, 'library/home.html')


def detail(request, pk, itemType=1):

    item = getItemDetails(pk, itemType)
    context = {
        "item": item[0],
        'similar': item[1]
    }

    return render(request, 'library/detail.html', context)

def detailMusic(request, pk):
    print(pk)
    item = getMusicDetails(pk, '1')

    context = {
        "item": item,
    }

    return render(request, 'library/detail_music.html', context)