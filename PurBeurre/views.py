
from django.shortcuts import render


def index(request):
    return render(request, 'templates/layouts/search.html')

def mentions(request):
    return render(request, 'templates/layouts/mentions.html')
