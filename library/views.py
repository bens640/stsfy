import json

from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView

from library.services import getThisYearMovies, searchMovies, getThisYearTv, getTopAlbums
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
    template_name = 'library/home.html'
    context_object_name = 'movies'

    def get_queryset(self):

        if self.request.GET.get('q'):
            query = self.request.GET.get('q')
        else:
            query = 'the'

        data = searchMovies(query)
        return data


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def add(request):
    val1 = request.POST.get('num1', None)
    print(val1)

    return render(request, 'library/home.html')
