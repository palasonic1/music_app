from django.db import models


class Artists(models.Model):
    name = models.CharField(max_length=255)
    img_url = models.URLField()
    spotify_id = models.CharField(max_length=64)
    genres = models.CharField(max_length=4096)

    @classmethod
    def get_or_none(cls, **kwargs):
        try:
            return cls.objects.get(**kwargs)
        except Artists.DoesNotExist:
            return None
