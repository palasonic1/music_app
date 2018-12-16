from django.conf.urls import url, include
from . import views

app_name = 'albums'
urlpatterns = [
    url(r'^feed', views.feed, name='feed'),
    url(r'^album', views.tracks_of_album, name='tracks_of_album'),
]

