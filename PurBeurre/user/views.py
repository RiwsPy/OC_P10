from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from catalogue.models import Favorite_product, Product
from collections import defaultdict
import re

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
    if request.user.is_authenticated:
        return account(request)

    print(context.get('msgs'))
    context['form'] = UserForm()
    return render(request, 'user/login.html', context)

@login_required(login_url='/user/login/')
def account(request):
    print('account')
    context = {
        'page_title': request.user.username,
    }
    return render(request, 'user/account.html', context)

def user_login(request):
    print('user_login')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return connexion(request, context={'msgs': ['Compte inconnu.']})

    return redirect('home')

@login_required(login_url='/')
def user_logout(request):
    print('user_logout')
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

regex_remove_tag = re.compile(r'<[^>]*>')

def register(request):
    if request.user.is_authenticated:
        print('user déjà connecté')
        return redirect('home')

    context = {'msgs': []}
    if request.method == 'GET':
        form = UserForm()
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            print('Le compte a été créé avec succès.')
            return redirect('home')

        context['msgs'].append('Compte non créé.')

    for msg in form.errors.values():
        msg = regex_remove_tag.sub('', str(msg))
        context['msgs'].append(msg)

    context['form'] = form
    return render(request, 'user/register.html', context)

@login_required(login_url='/user/login/')
def favorite(request):
    context= {}
    user_search = request.GET.get('user_search')
    if not user_search: # show Menu 1: product to substitute
        data = Favorite_product.objects.filter(user=request.user)

        db = set(product.product
            for product in data)

        if not db:
            context['msgs'] = "Aucun produit n'a encore été sauvegardé."

        context['db'] = db
        context['in_favorite_menu'] = True
    else: # show Menu 2: display substitute
        product_search = Product.objects.get(code=user_search)
        data = Favorite_product.objects.filter(
            user=request.user,
            product=user_search)

        context['product_id'] = product_search
        context['db'] = [product.substitute
            for product in data]

    context['page_title'] = 'Mes aliments'
    context['display_save_button'] = True

    return render(request, 'catalogue/result.html', context)

    #return render(request, 'user/favorite.html', context)
