from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', homepage, name='main'),
    url(r'^(?P<hashed_id>.)$', redirect_originalUrl, name='redirectOriginalUrl' ),
    url(r'^reduce/$', hashingUrl, name='hashing' )
]
