from django.contrib import admin


# Register your models here.
from .models import UrlHistory
admin.site.register(UrlHistory)

class Admin(admin.ModelAdmin):
    list_display = ('id', 'url_originalAddr','url_UrlHash', 'url_IdHash')
    #ordering = ('-id')

