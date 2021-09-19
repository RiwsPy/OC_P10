from django.core import paginator
from django.db.models.query import QuerySet, EmptyQuerySet
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Favorite_product, Product
from django.http import Http404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from typing import Tuple
from django.core.handlers.wsgi import WSGIRequest

# TODO: comment voir la fiche OFF d'un produit non substitué ?

# Create your views here.
def result(request: WSGIRequest) -> HttpResponse:
    if request.method != 'GET':
        return redirect(request.META['HTTP_REFERER'])

    user_search = request.GET.get('user_search', '')[:100]
    print('result', user_search)
    all_objects = []
    context = {
        'product_id': None, # to display the image product if any
        'paginate': False,
        'display_save_button': True,
        'msgs': [],
        'user_search': user_search,
    }

    # search by code then by name
    product_id = Product.objects.filter(code=user_search) or \
                 Product.objects.filter(product_name__icontains=user_search)

    if product_id.exists():
        if product_id.count() > 1: # too many search result : choice page
            all_objects = product_id
            product_id = None
            context['page_title'] = user_search
            context['msgs'].append('Plusieurs résultats correspondent à vos critères de recherche :')
        else:
            product_id = product_id[0]
            context['product_id'] = product_id
            context['msgs'].append('Vous pouvez remplacer cet aliment par :')
            context['page_title'] = product_id.product_name
            all_objects = ordered_substitute_food(product_id.code)

        # display paginate
        all_objects, context['paginate'] = paginate(request, all_objects)
    else:
        context['msgs'].append('Aucun produit ne correspond aux critères de recherche... :(')

    # display save_button
    display_save_button = product_id and request.user.is_authenticated
    if display_save_button:
        for product in all_objects:
            is_already_saved = Favorite_product.objects.filter(
                product=product_id.code,
                substitute=product.code,
                user=request.user.id)

            product.display_save = not bool(is_already_saved)

    context['db'] = all_objects
    context['display_save_button'] = display_save_button

    return render(request, 'catalogue/result.html', context)


@login_required(login_url='/user/login/')
def favorite_result(request: WSGIRequest) -> HttpResponse:
    if request.method != 'GET':
        return redirect(request.META['HTTP_REFERER'])

    user_search = request.GET.get('user_search', '')
    product_id = Product.objects.get(code=user_search)
    if not product_id:
        return redirect(request.META['HTTP_REFERER'])

    context = {
        'user_search': product_id,
        'product_id': product_id,
        'paginate': False,
        'display_save_button': True,
        'page_title':  product_id.product_name,
        'msgs': [],
    }

    # QuerySet with all substitute product
    all_objects = Favorite_product.objects.filter(
                    user=request.user,
                    product=product_id.code)

    # save all substitute code
    favorite_set = set()
    for favorite_product in all_objects:
        favorite_set.add(favorite_product.substitute.code)

    # search all substitute Product
    all_objects = Product.objects.filter(code__in=favorite_set)

    if all_objects.exists():
        all_objects, context['paginate'] = paginate(request, all_objects)
        # display delete_button
        for product in all_objects:
            product.display_save = False

    context['db'] = all_objects

    return render(request, 'catalogue/result.html', context)


def paginate(
            request: WSGIRequest,
            all_objects: QuerySet,
            nb_product_by_page: int=6) \
                -> Tuple[QuerySet, bool]:
    """
        Create and configure product paginate if necessary.
        * Up to ``nb_product_by_page`` can be used by page.
        * Tuple is returned, first element is ``all_objects`` with paginate (if any).
        * Second element is bool, True if paginate is created, False otherwise.
    """
    if all_objects.count() > nb_product_by_page:
        display_paginate = True
        paginator = Paginator(all_objects, nb_product_by_page)
        page = request.GET.get('page', 1)

        try:
            all_objects = paginator.page(page)
        except PageNotAnInteger:
            all_objects = paginator.page(1)
        except EmptyPage:
            all_objects = paginator.page(paginator.num_pages)
    else:
        display_paginate = False

    return all_objects, display_paginate

"""
def search(request: WSGIRequest) -> HttpResponse:
    print('search', request.method)
    return render(request, 'catalogue/search.html')
"""

def ordered_substitute_food(product_id: str) -> QuerySet:
    """
        Search ``product_id`` in Product db.
        Return ``EmptyQuerySet`` if is not found.
        Otherwise, in ``QuerySet`` return all products in the same category
        with nutrition score equal or better and sorted by
        nutrition score, nova group then eco score.
    """
    try:
        obj = Product.objects.get(pk=product_id)
    except ObjectDoesNotExist:
        db = EmptyQuerySet()
    else:
        db = Product.objects.filter(
                categories__exact=obj.categories.all()[0],
                nutrition_grades__lte=obj.nutrition_grades).\
                    exclude(pk=obj.code).\
                    order_by('nutrition_grades', 'nova_groups', 'eco_score')

    return db


def details(request: WSGIRequest, product_id: str) -> HttpResponse:
    print(product_id)
    context = {}
    try:
        product_id = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        context['msgs'] = ['Aucun produit ne correspond à vos critères de recherche.']
    else:
        context['product_id'] = product_id
        context['page_title'] = product_id.product_name

    return render(request, 'catalogue/details.html', context=context)


@login_required(login_url='/user/login/')
def save_product(request: WSGIRequest) -> HttpResponse:
    print('save', request.method, request.POST)
    if request.method != 'POST':
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    product_search_id = None
    if request.POST['product_search_id'] != '': # delete saved product
        product_search_id = Product.objects.get(code=request.POST['product_search_id'])

    substitute_id = Product.objects.get(code=request.POST['substitute_id'])

    if not substitute_id:
        return redirect(request.META['HTTP_REFERER'])

    context = {}
    if not product_search_id: # delete saved product
        already_saved = Favorite_product.objects.filter(
                user=request.user,
                product=request.POST['substitute_id'])
    else:
        already_saved = Favorite_product.objects.filter(
                user=request.user,
                product=request.POST['product_search_id'],
                substitute=request.POST['substitute_id'])

    if already_saved:
        already_saved.delete()
        context['msgs'] = 'Produit retiré avec succès.'
        print('Produit supprimé.')
    elif product_search_id:
        new_favorite_product = Favorite_product()
        new_favorite_product.product = product_search_id
        new_favorite_product.substitute = substitute_id
        new_favorite_product.user = request.user
        new_favorite_product.save()
        context['msgs'] = 'Produit sauvegardé avec succès.'
        print('Produit sauvegardé')
    else:
        print('error')

    return redirect(request.META['HTTP_REFERER'], context=context)
