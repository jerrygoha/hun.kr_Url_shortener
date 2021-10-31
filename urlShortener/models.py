from django.db import models

class UrlHistory(models.Model):
    url_originalAddr = models.URLField(max_length=300)
    url_encodedAddr = models.URLField(default="")
    url_createdDate = models.DateTimeField(auto_now_add=True)
    url_visitedCount = models.IntegerField(default=0)

    def __str__(self):
        return self.url_originalAddr

