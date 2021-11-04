import hashlib
import math
import json
import logging

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from .models import UrlHistory


def homepage(request):
    """메인 페이지"""

    return render(request, 'urlShortener/index.html')


def redirect_originalUrl(request, hashed_id):
    """shorten url을 입력받으면 redirect 시켜준다."""

    base10_id = __make_base10(hashed_id)
    url = get_object_or_404(UrlHistory, id=base10_id)
    return HttpResponseRedirect(url.url_originalAddr)


def hashingUrl(request):
    """입력받은 url을 줄이는 기능"""

    original_url = __rebuild_Url(request.POST.get("url", ''))

    # if not (original_url == ""):
    url_UrlHash = __make_md5(original_url)

    # 입력받은 주소가 db에 존재하는지 체크
    try:
        _url = UrlHistory.objects.get(url_UrlHash=url_UrlHash)
    except:
        _url = None

    # 새로운 주소일 경우 url과 id의 해시값을 db에 저장
    if _url is None:
        db_input = UrlHistory(url_originalAddr=original_url, url_UrlHash=url_UrlHash)
        db_input.save()

        # db에 저장 이후 생긴 id값을 가져와 id_hash값 도출
        temp_obj = UrlHistory.objects.get(url_originalAddr=original_url)
        id_IdHash = __make_base62(temp_obj.id)
        # db에 저장하게된다면 살릴 코드
        # temp_obj.url_IdHash = id_IdHash
        # temp_obj.save()

    # 이미 등록되어있는 주소일 경우 단순반환
    else:
        id_IdHash = __make_base62(UrlHistory.objects.get(url_originalAddr=original_url).id)

    response = {}
    response["url"] = settings.SITE_URL + "/" + id_IdHash
    return HttpResponse(json.dumps(response), content_type="application/json")
# return HttpResponse(json.dumps({"error": "error!!"}), content_type="application/json")


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

    if "http://" in input_url:
        return input_url
    elif "https://" in input_url:
        return "http://" + input_url[8:]
    else:
        return "http://" + input_url
