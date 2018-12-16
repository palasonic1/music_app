from django.conf.urls import url, include
from . import views

app_name = 'albums'
urlpatterns = [
    url(r'^feed', views.feed, name='feed'),
    #url(r'^search_artists', views.search_artists, name='search_artists'),
    #url(r'^favorite_artists', views.favorite_artists, name='favorite_artists'),
]

