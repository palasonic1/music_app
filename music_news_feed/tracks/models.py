from django.db import models
from albums.models import Albums
from artists.models import Artists


class Tracks(models.Model):
    name = models.CharField(max_length=255)
    album = models.ForeignKey(Albums, on_delete=models.SET_NULL())
    artists = models.ManyToManyField(Artists)
    track_number = models.SmallIntegerField()
    disc_number = models.SmallIntegerField()
    duration_ms = models.IntegerField()
    spotify_id = models.CharField(max_length=64)
    preview_url = models.URLField()
