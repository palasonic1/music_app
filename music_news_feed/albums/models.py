from django.db import models
from enum import Enum
from artists.models import Artists
from django.contrib.auth.models import User


class AlbumTypes(Enum):
    LP = 'album'
    SP = 'single'
    CP = 'compilation'


class Albums(models.Model):
    name = models.CharField(max_length=255)
    album_type = models.CharField(max_length=15, choices=[(tag, tag.value) for tag in AlbumTypes])
    genres = models.CharField(max_length=4096)
    spotify_id = models.CharField(max_length=64)
    img_url = models.URLField(blank=True)
    release_date = models.DateField()
    artists = models.ManyToManyField(Artists)
    users = models.ManyToManyField(User, through='Updates', related_name='album_updates')

    @classmethod
    def get_or_none(cls, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except Albums.DoesNotExist:
            return None


class Updates(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Albums, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
