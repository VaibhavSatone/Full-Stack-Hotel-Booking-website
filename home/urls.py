from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('',home,name='home'),
    path('login',login_page,name='login_page'),
    path('Register',register_page,name='register_page'),
    path('logout',logout_page,name="logout"),
    path('search',search_page,name="search_page"),
]

