from django.db import models
from enum import Enum
from artists.models import Artists


class AlbumTypes(Enum):
    LP = 'album'
    SP = 'single'
    CP = 'compilation'


class Albums(models.Model):
    name = models.CharField(max_length=255)
    album_type = models.CharField(max_length=15, choices=[(tag, tag.value) for tag in AlbumTypes])
    genres = models.CharField(max_length=4096)
    spotify_id = models.CharField(max_length=64)
    img_url = models.URLField()
    release_date = models.DateField()
    artists = models.ManyToManyField(Artists)
