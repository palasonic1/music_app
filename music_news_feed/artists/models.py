from django.db import models


class Artists(models.Model):
    name = models.CharField(max_length=255)
    img_url = models.URLField()
    spotify_id = models.CharField(max_length=64)
    genres = models.CharField(max_length=4096)
