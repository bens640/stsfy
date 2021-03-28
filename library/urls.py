from django.conf.urls import url
from django.urls import path
from . import views
from .views import SearchResultsView, TestPage

urlpatterns = [
    path('', views.home, name='library-home'),
    path('test/', views.testPage, name='library-test'),
    # path('test/', TestPage.as_view(), name='library-test'),

    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('detail/<int:pk>/', views.detail, name='detail'),
    path('detail/<int:pk>/<str:itemType>/', views.detail, name='detail'),
    path('detail/music/<str:pk>', views.detailMusic, name='detail-music'),
    path('detail/person/<int:pk>/', views.personDetail, name='detail-person'),
    path('tv/', views.tvPage, name='library-tv'),
    path('movie/', views.moviePage, name='library-movie'),
    path('music/', views.musicPage, name='library-music'),
    path('test/filter/', views.filter, name='filter'),

]