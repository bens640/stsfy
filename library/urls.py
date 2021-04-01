from django.conf.urls import url
from django.urls import path
from . import views
from .views import SearchResultsView, TestPage, GroupCreateView, GroupListView, GroupDetailView

urlpatterns = [
    path('', views.home, name='library-home'),
    path('test/', views.testPage, name='library-test'),
    # path('test/', TestPage.as_view(), name='library-test'),

    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('detail/<int:pk>/<str:itemType>/', views.detail, name='detail'),
    path('detail/music/artist<str:pk>', views.detailArtistMusic, name='detail-artist-music'),
    path('detail/music/album<str:pk>', views.detailAlbumMusic, name='detail-album-music'),
    path('detail/person/<int:pk>/', views.personDetail, name='detail-person'),
    path('tv/', views.tvPage, name='library-tv'),
    path('movie/', views.moviePage, name='library-movie'),
    path('music/', views.musicPage, name='library-music'),
    path('test/filter/<str:type>/', views.filter, name='filter'),
    path('groups/', GroupListView.as_view(), name='groups'),
    path('group/new/', GroupCreateView.as_view(), name='group-create'),
    path('group/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),

]