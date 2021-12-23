from django.urls import path, include
from . import views 

app_name = 'player'
urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('home', views.IndexView.as_view(), name='home'),
    path('index', views.IndexView.as_view(), name='index'),
    ]