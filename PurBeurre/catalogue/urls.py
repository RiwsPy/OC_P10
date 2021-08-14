from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.result, name='result'),
    path('search/', views.search, name='home'),
    path('save/', views.save, name='save'),
    re_path(r'([0-9]+)/details/', views.details, name='details'),
    re_path(r'([0-9]+)/', views.result, name='result'),
]
