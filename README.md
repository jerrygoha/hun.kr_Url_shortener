## Url_shortener
사용자가 입력한 url을 숫자와 문자(영문)이 섞인 8자리 이하의 문자로 축약시켜주는 서비스
- 같은 url 입력시 동일한 결과값 출력
- http://, https:// 정도는 같은 주소로 취급하도록 함
  - www. 여부 또는 대소문자 차이 같은 경우는 예외가 있을 수 있으므로 다른 주소로 취급
- 정상적인 url 형식을 벗어난 경우, 오류 메시지 출력
  - 도메인 형식이 다양하므로 예외 발생 가능성 있음

## Preview
<img width="100%" src="https://user-images.githubusercontent.com/48903443/140506937-34611364-6614-4198-ab25-1e50e661a859.gif"/>


<a href="https://youtu.be/OZXnNHopzME" target="_blank">영상으로 보기<a>


## Prerequisite
```
Python    == 3.7.8
pip       == 21.3.1
asgiref   == 3.4.1
Django    == 3.2.8
pytz      == 2021.3
sqlparse  == 0.4.2
typing-extensions == 3.10.0.2
```

## Usage in Local

```

> git clone https://github.com/jerrygoha/hun.kr_Url_shortener.git

> cd hun.kr_Url_shortener

> pip install django

> python manage.py makemigrations urlShortener

# 모델의 변경사항 번호(number) 체크 필요
> python manage.py migrate urlShortener {number}

> python manage.py runserver

```


## API
### Main Page
|Role|Api|Parameter|
|---|---|---|
|Home Page|GET&nbsp;&nbsp;&nbsp;&nbsp;/|None|
|Send Url|POST&nbsp;&nbsp;&nbsp;&nbsp;/&nbsp;shorten&nbsp;/|Url(original)|

   - GET
```
  "GET / HTTP/1.1" 200 1626
```
   - POST
```
  "POST /shorten/ HTTP/1.1" 200 35
```


### Redirect Shortened Url
|Role|Api|Parameter|
|---|---|---|
|Redurect Original Url|GET&nbsp;&nbsp;&nbsp;&nbsp;/{shortened_url}|shortened_url value example : e92J9k|

- Success Responce
```
  "GET /1n HTTP/1.1" 302 0
```

- Failure Response
```
  "GET /1nasd HTTP/1.1" 404 179
```


## TO-DO
1. URL Shortener (Main)
   - 웹 페이지 입력폼에 URL 입력 시 단축된 결과 출력
   - 브라우저의 주소창에 단축 URL 입력 시 기존 URL로 리다이렉트
   - 같은 URL 입력 시 동일한 결과값 도출
   - 결과값은 주소를 제외하고 8글자 이내로 생성
   
## HOW TO...
1. URL Shortener
   1. 브라우저 주소창에 단축 URL 입력 시 기존 URL로 리다이렉트
      > http 302 redirection 사용.
   2. 같은 URL 입력 시 동일한 결과값 도출
      > md5 인코딩 후 DB에서 비교, 중복인 경우 기존 id값을 참고하여 결과값 도출
   3. 결과값은 주소를 제외하고 8글자 이내로 생성
      > 튜플의 id값을 base62로 인코딩하여 출력
2. DB
   1. ORM vs raw sql
      > ORM 사용 
   2. 비용 최소한으로
      > DB에 접속하는 비용 vs 파이썬 인코딩/디코딩 함수 돌리는 비용
