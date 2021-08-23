from django.core import paginator
from django.db.models.query import QuerySet
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Favorite_product, Product
from django.http import Http404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError

# Create your views here.
def result(request):
    if request.method != 'GET':
        return redirect(request.META['HTTP_REFERER'])

    user_search = request.GET.get('user_search', '')[:100]
    print(user_search)
    all_objects = []
    context = {
        'user_search': user_search,
        'product_id': None,
        'paginate': False,
        'display_save_button': True,
    }

    # search by code then by name
    product_id = Product.objects.filter(code=user_search) or \
                 Product.objects.filter(product_name__icontains=user_search)

    if product_id.exists():
        # too many search result : choice page
        if product_id.count() > 1:
            all_objects = product_id
            product_id = None
        else:
            product_id = product_id[0]
            context['product_id'] = product_id
            all_objects = ordered_substitute_food(product_id.code)

        # display paginate
        all_objects, context['paginate'] = paginate(request, all_objects)

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
def favorite_result(request):
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
    }

    # QuerySet with all substitute product
    all_objects = Favorite_product.objects.filter(
                    user=request.user,
                    product=product_id.code)
    favorite_set = set()
    for favorite_product in all_objects:
        favorite_set.add(favorite_product.substitute.code)
    all_objects = Product.objects.filter(code__in=favorite_set)

    if all_objects.exists():
        all_objects, context['paginate'] = paginate(request, all_objects)
        # display delete_button
        for product in all_objects:
            product.display_save = False

    context['db'] = all_objects

    return render(request, 'catalogue/result.html', context)


def paginate(request, all_objects, nb_product=6):
    if all_objects.count() > nb_product:
        display_paginate = True
        paginator = Paginator(all_objects, nb_product)
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


def search(request):
    print('search', request.method)
    return render(request, 'catalogue/search.html')


def ordered_substitute_food(product_id) -> QuerySet:
    try:
        obj = Product.objects.get(pk=product_id)
    except ObjectDoesNotExist:
        db = []
    else:
        db = Product.objects.\
            filter(nutrition_grades__lte=obj.nutrition_grades).\
            filter(categories__exact=obj.categories.all()[0]).\
            exclude(pk=obj.code).\
            order_by('nutrition_grades', 'nova_groups', 'eco_score')

    return db

def details(request, product_id):
    print(product_id)
    product_id = Product.objects.get(pk=product_id)
    # if not product_id.exists():
    context = {'id': product_id}
    return render(request, 'catalogue/details.html', context=context)

@login_required(login_url='/user/login/')
def save_product(request):
    print('save', request.method, request.POST)
    if request.method != 'POST':
        return redirect(request.META['HTTP_REFERER'])

    product_search_id = Product.objects.get(code=request.POST['product_search_id'])
    substitute_id = Product.objects.get(code=request.POST['substitute_id'])
    if not substitute_id or not product_search_id:
        return redirect(request.META['HTTP_REFERER'])

    already_saved = Favorite_product.objects.filter(
            user=request.user,
            product=request.POST['product_search_id'],
            substitute=request.POST['substitute_id'])

    if already_saved:
        already_saved.delete()
        print('Produit supprimé.')
    else:
        new_favorite_product = Favorite_product()
        new_favorite_product.product = product_search_id
        new_favorite_product.substitute = substitute_id
        new_favorite_product.user = request.user
        new_favorite_product.save()
        print('Produit sauvegardé')

    return redirect(request.META['HTTP_REFERER'])