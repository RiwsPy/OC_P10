from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm

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

def connexion(request, context={}):
    print('connexion')
    return render(request, 'user/connexion.html', context=context)

def account(request):
    print('account')
    return render(request, 'user/account.html')

def user_login(request):
    print('user_login')
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
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
