
from django.shortcuts import render


def index(request):
    return render(request, 'PurBeurre/templates/layouts/search.html')

def mentions(request):
    return render(request, 'PurBeurre/templates/layouts/mentions.html')
