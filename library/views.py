from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'library/home.html')


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
