from django.conf.urls import url
from django.urls import path
from . import views
from .views import SearchResultsView,  GroupCreateView, GroupListView, GroupDetailView

urlpatterns = [
    path('', views.home, name='library-home'),
    path('test/', views.testPage, name='library-test'),
    # path('test/', TestPage.as_view(), name='library-test'),

    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('detail/<int:pk>/<str:itemType>/', views.detail, name='detail'),
    path('detail/music/artist<str:pk>/<str:itemType>/', views.detailArtistMusic, name='detail-artist-music'),
    path('detail/music/album<str:pk>', views.detailAlbumMusic, name='detail-album-music'),
    path('detail/person/<int:pk>/', views.personDetail, name='detail-person'),
    path('tv/', views.tv_page, name='library-tv'),
    path('movie/', views.movie_page, name='library-movie'),
    path('music/', views.music_page, name='library-music'),
    path('groups/', GroupListView.as_view(), name='groups'),
    path('group/new/', GroupCreateView.as_view(), name='group-create'),
    path('group/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),

]