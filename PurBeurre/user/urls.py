from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('connexion/', views.index, name='connexion'),
    path('account/', views.account, name='account'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('favorite/', views.favorite, name='favorite'),
]
