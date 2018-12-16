from django.contrib.auth.models import User
from django.db import models


class Artists(models.Model):
    name = models.CharField(max_length=255)
    img_url = models.URLField(blank=True)
    spotify_id = models.CharField(max_length=64)
    genres = models.CharField(max_length=4096)
    users = models.ManyToManyField(User, through='Preferences', related_name='artists_preferences')

    @classmethod
    def get_or_none(cls, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except Artists.DoesNotExist:
            return None


class Preferences(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artists, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
