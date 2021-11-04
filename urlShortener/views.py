import hashlib
import math
import json
import logging

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import UrlHistory


# 메인페이지
def homepage(request):
    return render(request, 'urlShortener/index.html')

# redirect function
def redirect_originalUrl(request, hashed_id):
    url = get_object_or_404(UrlHistory, url_IdHash=hashed_id)
    return HttpResponseRedirect(url.url_originalAddr)

# hashing and create function
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
    original_url = __rebuild_Url(request.POST.get("url", ''))
    if not (original_url == ""):
        url_UrlHash = __make_md5(original_url)
        #입력받은 주소가 db에 존재하는지 체크
        try:
            _url = UrlHistory.objects.get(url_UrlHash=url_UrlHash)
        except:
            _url = None

        # 새로운 주소일 경우 url과 id의 해시값을 db에 저장
        if _url is None: 
            db_input = UrlHistory(url_originalAddr=original_url, url_UrlHash=url_UrlHash)
            db_input.save()

            # save hashed_id
            temp_obj = UrlHistory.objects.get(url_originalAddr=original_url)
            id_IdHash = __make_base62(temp_obj.id)
            temp_obj.url_IdHash = id_IdHash
            temp_obj.save()
        # 이미 등록되어있는 주소일 경우 단순반환
        else: 
            id_IdHash = UrlHistory.objects.get(url_originalAddr=original_url).url_IdHash
        response = {}
        response["url"] = settings.SITE_URL + "/" + id_IdHash
        return HttpResponse(json.dumps(response), content_type="application/json")
    return HttpResponse(json.dumps({"error": "error!!"}), content_type="application/json")


def __make_md5(original_url):
    """original_url을 md5로 인코딩한다."""
    input_url = original_url.encode('utf-8')
    tmp = hashlib.md5()
    tmp.update(input_url)
    result = tmp.hexdigest()
    return result


def __make_base62(url_id):
    """id를 base62로 인코딩한다."""
    base62_char = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    char_cnt = url_id % 62
    result = base62_char[char_cnt]
    char_cnt_floor = math.floor(url_id / 62)
    while char_cnt_floor:
        char_cnt = char_cnt_floor % 62
        char_cnt_floor = math.floor(char_cnt_floor / 62)
        result = base62_char[int(char_cnt)] + result
    return result

def __make_base10(input):
    """base62 id_hash 를 10진수로 디코딩"""
    base62_char = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = 0
    for i in input:
        result = 62 * result + base62_char.find(i)
    return result


def __rebuild_Url(input):
    """
        1. original_url 에 http://가 포함되어있지 않다면 붙여준다.
           사이트에 ssl 인증서가 있다면 자동으로 https://로 전환된다.
        2. url 마지막 문자가 "/" 라면 지워준다.
    """
    input_url = input
    if input_url[-1] is "/":
        input_url = input_url[:-1]

    if "http://" in input_url or "https://" in input_url:
        return input_url
    else:
        return "http://"+input_url

