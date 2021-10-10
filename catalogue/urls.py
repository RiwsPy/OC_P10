from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.result, name='result'),
    path('favorite/result/', views.favorite_result, name='favorite_result'),
    # path('search/', views.search, name='search'),
    path('save/', views.save_product, name='save'),
    path('delete/', views.delete_product, name='delete'),
    re_path(r'([0-9]+)/', views.details, name='details'),
]
