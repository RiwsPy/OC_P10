from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='home'),
    re_path(r'([0-9]+)/save/', views.save, name='save'),
    re_path(r'([0-9]+)/details/', views.details, name='details'),
    re_path(r'([0-9]+)/', views.index, name='index'),
]
