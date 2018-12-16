from django.conf.urls import url, include
from . import views

app_name = 'artists'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^add_user', views.add_user, name='add_user'),
]

