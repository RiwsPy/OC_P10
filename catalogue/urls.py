from django.urls import path, re_path
from catalogue import views

urlpatterns = [
    path('', views.result, name='result'),
    path('save/', views.save_product, name='save'),
    path('delete/', views.delete_product, name='delete'),
    re_path(r'([0-9]+)/', views.details, name='details'),
]
