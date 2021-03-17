from django.http import HttpResponse
from django.shortcuts import render

from library.services import getShowData


def home(request):
    x = getShowData()

    return render(request, 'library/home.html',{"media": x})


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
