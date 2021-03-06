from django.conf.urls import url, include
from . import views

app_name = 'artists'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search_artists', views.search_artists, name='search_artists'),
    url(r'^favorite_artists', views.favorite_artists, name='favorite_artists'),
]

