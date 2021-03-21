from django.conf.urls import url
from django.urls import path
from . import views
from .views import SearchResultsView

urlpatterns = [
    path('', views.home, name='library-home'),
    path('test/', views.testPage, name='library-test'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('test/add', views.add, name='library-add')

]