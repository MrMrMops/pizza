from django.contrib import admin

from django.urls import path
from order.views import *
from django.views.decorators.cache import cache_page
from pizzaweb import settings

urlpatterns = [
    path('',Index.as_view(), name='index'),
    path('add_post/',AddPostFormView.as_view(),name='add_post'),
    path('post/<slug:post_slug>/', PostView.as_view(),name='post'),
    path('login/',LoginUser.as_view(),name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/',RegisterUser.as_view(),name='register'),
    path('recall/',AboutViewForm.as_view(),name='recall')
]