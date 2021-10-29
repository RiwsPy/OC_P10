from django.urls import path
from user import views

urlpatterns = [
    path('', views.index),
    path('login/', views.index, name='login'),
    path('account/', views.account, name='account'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('favorite/', views.favorite, name='favorite'),
]
