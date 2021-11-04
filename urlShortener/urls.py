from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', homepage, name='main'),
    # admin, reduce로 시작하지 않고, 1자리부터 8자리 사이의 자릿수로 base62 문자가 들어가면 매치.
    url(r'^(?!^admin|^shorten)(?P<hashed_id>.{1,8})$', redirect_originalUrl, name='redirectOriginalUrl' ),
    url(fr'^shorten/$', hashingUrl, name='hashing' )
]
