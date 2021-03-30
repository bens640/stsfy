import json
from dateutil.parser import *
from dateutil.utils import today

from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, CreateView, DetailView

from library.services import *
from stsfy.settings import TMDB_API
from users.models import Group, Membership

movie_genre_list = {"28": "Action", "12": "Adventure", '16': 'Animation', '35': 'Comedy', '80': 'Crime',
                    '99': 'Documentary', '18': 'Drama', '10751': 'Family', '14': 'Fantasy', '36': 'History',
                    '27': 'Horror',
                    '10402': 'Music', '9648': 'Mystery', '10749': 'Romance', '878': 'Science Fiction',
                    '10770': 'TV Movie',
                    '53': 'Thriller', '10752': 'War', '37': 'Western', }


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
    genre_lists = movie_genre_list

    data = {
        "movies": movies,
        'tv': tv,
        'music': music,
        'item': item[0],
        'genre_list': genre_lists

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
    if 'next_episode_to_air' in item[0].info():
        if item[0].info()['next_episode_to_air'] is not None:
            next_air = parse(item[0].info()['next_episode_to_air']['air_date']).strftime('%A' + ', %b %d, %Y')
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
        'release': release_date
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
    tv = getThisYearTv()
    context = {
        'tv': tv
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
    genre_lists = movie_genre_list

    movies = getThisYearMovies()
    # genres = request.POST.getlist('genres')
    genres = ', '.join([str(elem) for elem in request.POST.getlist('genres')])

    filter_request = request.POST.copy()

    if request.method == 'POST':
        filter_request.pop("csrfmiddlewaretoken")
        if request.POST.get("genres"):
            filter_request.pop("genres")
        filter_request['with_genres'] = genres
        print(filter_request.dict())

    movies = tmdb.Discover().movie(**filter_request)

    data = {
        "movies": movies,
        'genre_list': genre_lists,
    }

    return render(request, 'library/test.html', data)


class GroupCreateView(CreateView):
    model = Group
    template_name = 'library/group_form.html'
    fields = ['name', 'about']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class GroupListView(ListView):
    model = Group
    context_object_name = 'groups'
    template_name = 'library/groups.html'


class GroupDetailView(DetailView):
    model = Group
    template_name = 'library/group_detail.html'

    def post(self, request, *args, **kwargs):
        print(self.kwargs.get('pk'))

        if Group.objects.get(id=self.kwargs.get('pk')):
            m1 = Membership(person=request.user, group=Group.objects.get(id=self.kwargs.get('pk')), date_joined=today())
            m1.save()
        return redirect('groups')

    def get_context_data(self, **kwargs):
        group = Group.objects.get(pk=self.kwargs.get('pk'))
        # shows = StShow.objects.filter(group=group)
        context = {'group': group,
                   'users': group.members.all(),
                   # 'shows': shows
                   }
        return context
