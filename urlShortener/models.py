from django.db import models
from django.urls import reverse

class UrlHistory(models.Model):
    url_originalAddr = models.URLField(max_length=500)
    url_UrlHash = models.CharField(max_length=500, default="")
    url_IdHash = models.CharField(max_length=8, default="")

    def __str__(self):
        return self.url_originalAddr

    def get_absolute_url(self):
        return reverse('detail', args=[self.id])