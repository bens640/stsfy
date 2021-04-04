import json
from dateutil.parser import *
from dateutil.utils import today

from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, CreateView, DetailView

from library.models import Item, UserItem
from library.services import *
from stsfy.settings import TMDB_API
from users.models import Group, Membership
from .services import add_item


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
    genre_lists = getGenres('movie')
    items = UserItem.objects.filter(owned_by=request.user)
    unused_items = UserItem.objects.filter(owned_by=request.user, consumed=False)
    used_items = UserItem.objects.filter(owned_by=request.user, consumed=True)
    data = {
        "movies": movies,
        'tv': tv,
        'music': music,
        'item': item[0],
        'items': items,
        'genre_list': genre_lists,
        'unused_items': unused_items,
        'used_items': used_items

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
    x = getUserItem(request, pk)
    current_item = []
    if x[1]: current_item = x[1][0]

    if request.user.is_authenticated:
        others_watching = UserItem.objects.filter(item=x[0]).exclude(owned_by=request.user)
    else:
        others_watching= []

    if 'next_episode_to_air' in item[0].info():
        if item[0].info()['next_episode_to_air'] is not None:
            next_air = parse(item[0].info()['next_episode_to_air']['air_date']).strftime('%A' + ', %b %d, %Y')
        else:
            next_air = None
    if 'release_date' in item[0].info():
        if item[0].info()['release_date'] is not None:
            release_date = parse(item[0].info()['release_date']).strftime('%A' + ', %b %d, %Y')

    if request.POST.get('add_item', ""):
        add_item(request, item[0], itemType)

        return redirect(detail, item[0].id, itemType)
    elif request.POST.get('remove_item', ""):
        remove_item(request, item[0])
        return redirect(detail, pk, itemType)
    elif request.POST.get('add_group', ""):
        group_name = request.POST.get('group_add', "")
        toggle_group(request, pk, group_name)

    if request.POST.get('consumed', ""):
        current_item.consumed ^= True
        current_item.save()
    context = {
        "item": item[0],
        'similar': item[1],
        'credits': item[2],
        'airdate': next_air,
        'release': release_date,
        'owned': x[1],
        'other_watching': others_watching,
        'groups': x[2],
        'current_item': current_item,
    }

    return render(request, 'library/detail.html', context)


def detailArtistMusic(request, pk , itemType='1'):
    item = getMusicDetails(pk, '1')
    albums = getMusicDetails(pk, '2')
    x = getUserItem(request, pk)

    current_item = []
    if x[1]: current_item = x[1][0]

    if request.POST.get('add_item', ""):
        add_music_item(request, pk, itemType)
        return redirect(detailArtistMusic, pk, 1)
    elif request.POST.get('remove_item', ""):
        remove_music_item(request, pk)
        return redirect(detailArtistMusic, pk)
    elif request.POST.get('add_group', ""):
        group_name = request.POST.get('group_add', "")
        toggle_group(request, pk, group_name)
    if request.user.is_authenticated:
        others_listening = UserItem.objects.filter(item=x[0]).exclude(owned_by=request.user)
    else:
        others_listening = []
    context = {
        "item": item,
        'albums': albums,
        'groups': x[2],
        'current_item': current_item,
        'others_listening': others_listening,
        'owned': x[1],
    }

    return render(request, 'library/detail_music_artist.html', context)


def detailAlbumMusic(request, pk):
    sp = spotify.album(pk)

    context = {
        "item": sp,

    }

    return render(request, 'library/detail_music_album.html', context)


def personDetail(request, pk):
    person = getPersonDetail(pk)

    context = {
        'details': person[0],
        'credits': person[1]
    }
    return render(request, 'library/person_detail.html', context)


def movie_page(request):
    sort_filter = add_filter(request, 'movie')
    context = {
        'movies': sort_filter[1],
        'genre_list': sort_filter[0],
    }
    return render(request, 'library/movie_page.html', context)


def tv_page(request):
    sort_filter = add_filter(request, 'tv')
    context = {
        'tv': sort_filter[2],
        'genre_list': sort_filter[0],
    }
    return render(request, 'library/tv_page.html', context)


def music_page(request):
    music = getTopAlbums()
    sort_filter = add_music_filter(request)
    context = {
        'music': sort_filter[1],
        'categories': sort_filter[0]
    }
    return render(request, 'library/music_page.html', context)


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
        group_items = UserItem.objects.filter(group=group)
        context = {'group': group,
                   'users': group.members.all(),
                   'items': group_items,
                   }
        return context
