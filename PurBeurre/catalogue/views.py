from django.core import paginator
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Favorite_product, Product
from django.http import Http404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.
def result(request, product_name='', page=1):
    # raise Http404("Sorry... This page doesn't exist.")
    if request.method != 'GET':
        return redirect('home')

    product_name = request.GET.get('product_search', '')

    print('result', request.method, product_name)
    # search by name
    product_id = Product.objects.filter(product_name__icontains=product_name)

    # search by code
    if not product_id.exists():
        product_id = Product.objects.filter(code=product_name)

    if product_id.count() != 1:
        all_objects = product_id
        product_id = None
    else:
        product_id = product_id[0]
        all_objects = ordered_substitute_food(product_id.code)

    paginator = Paginator(all_objects, 6)
    page = request.GET.get('page', 1)

    try:
        all_objects = paginator.page(page)
    except PageNotAnInteger:
        all_objects = paginator.page(1)
    except EmptyPage:
        all_objects = paginator.page(paginator.num_pages)

    context = {
        'search_product': product_name,
        'id': product_id,
        'db': all_objects,
        'paginate': True,
    }
    return render(request, 'catalogue/result.html', context)

def search(request):
    print('search', request.method)
    return render(request, 'catalogue/search.html')

def ordered_substitute_food(product_id):
    try:
        obj = Product.objects.get(pk=product_id)
    except ObjectDoesNotExist:
        db = None
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
def save(request):
    if request.method != 'POST':
        return redirect('home')

    print('okk')
    new_favorite_product = Favorite_product()
    new_favorite_product.save(
        product=Product.objects.get(request.POST['product_id']),
        substitute=Product.objects.get(request.POST['substitute_id']),
        user=request.user
    )
    print('lala')
    
    print(new_favorite_product)
    print('produit sauvegardé')
    return redirect('account')
