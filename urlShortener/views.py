from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import UrlHistory
from django.views.generic.edit import CreateView

#main page
@csrf_exempt
def homepage(request):
    return render(request, 'urlShortener/index.html')

# redirect function
def redirect_originalUrl(request, url_IdHash):
    url = get_object_or_404(UrlHistory, )
    return None

# hashing function
"""
<1.먼저 두 형태로 hashing한다.>
ㅣ---- url hashing : md5 hashing 사용 (동일한 입력값에 대해 결과가 항상 같기때문.)
ㅣ---- id hashing : base62 hashing 사용
why? : url은 길이가 굉장히 길기때문에 crc32, md5, 또는 커스텀 알고리즘을 만들어 해싱하는 경우
        결과값이 중복될 가능성이 있다.
        하지만, id값(int)은 base62(1~9, a~z, A~Z)를 사용하여 8자리 이내에서 중복없이 표현이 가능하다.
        단, 일어날 수 있는 동시성 문제에 대해서는 실제 서비스에 미치는 영향이 미미하다 판단하여 고려하지 않는다.

<2. url 중복체크 (md5)>
db 내에서 긴 길이의 url끼리 중복체크를 하는것보다, 해싱된 문자를 비교하는게 비용이 더 저렴.
다만, 다른 url끼리 해싱값이 같을 수 있으니, 해싱값이 같은 경우 original_url도 중복체크한다.(확률이 낮으므로 큰 비용 소모되지 않을듯하다.)
해싱값이 같고, original_url도 같다면 완전히 중복되므로, 기존 original_url의 id 해싱값을 리턴한다.
"""
def hashingUrl(request):
    return None