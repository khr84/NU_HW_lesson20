from django.contrib import admin
from django.urls import path
from hh_search_app import views

app_name = 'hh_search_app'

urlpatterns = [
    path('', views.main_view, name='index'),
    path('search/', views.search_view, name='search'),
    path('result/', views.result_view, name='result'),
    path('history/', views.history_view, name='history'),
]
