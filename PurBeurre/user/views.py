from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from catalogue.models import Favorite_product
from collections import defaultdict

# Create your views here.
def index(request):
    print(request.method)
    if request.user.is_authenticated:
        return account(request)
    else:
        if request.method == 'GET':
            return connexion(request)
        elif request.method == 'POST':
            return user_login(request)

def connexion(request):
    print('connexion')
    context = {'form': UserForm()}
    return render(request, 'user/connexion.html', context=context)

def account(request):
    print('account')
    return render(request, 'user/account.html')

def user_login(request):
    print('user_login')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return connexion(HttpRequest(), context={'msg': 'Compte inconnu.'})

    return redirect('home')

def user_logout(request):
    print('user_logout')
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

def register(request):
    if request.user.is_authenticated:
        print('user déjà connecté')
        return redirect('home')

    if request.method == 'GET':
        form = UserForm()
    else:
        form = UserForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            print('le compte a été créé avec succès.')
            return redirect('home')

        print('compte non créé')

    return render(request, 'user/register.html', context={'form': form})

@login_required(login_url='/user/login/')
def favorite(request):
    ret = Favorite_product.objects.filter(user=request.user)

    product_set = set()
    for product in ret:
        product_set.add(product.product)

    dict_ret = {}
    for product_id in product_set:
        dict_ret[product_id] = ret.filter(product=product_id)

    context= {'db': dict_ret, 'page_title': 'Mes aliments'}
    return render(request, 'user/favorite.html', context)
