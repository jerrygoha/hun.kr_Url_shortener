# Url_shortener

## Description
사용자가 입력한 url을 숫자와 문자(영문)이 섞인 8자리 이하의 문자로 축약시켜주는 서비스
- 같은 url 입력시 동일한 결과값 출력
- http://, https:// 정도는 같은 주소로 취급하도록 함
  - www. 여부 또는 대소문자 차이 같은 경우는 예외가 있을 수 있으므로 다른 주소로 취급
- 정상적인 url 형식을 벗어난 경우, 오류 메시지 출력
  - 도메인 형식이 다양하므로 예외 발생 가능성 있음

## Preview
<img width="100%" src="https://user-images.githubusercontent.com/48903443/140506937-34611364-6614-4198-ab25-1e50e661a859.gif"/>

<a href="https://youtu.be/bDvSCpXsqMU" target="_blank">영상으로 보기<a>


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
1. URL Shortener
   - 웹 페이지 입력폼에 URL 입력 시 단축된 결과 출력
   - 브라우저의 주소창에 단축 URL 입력 시 기존 URL로 리다이렉트
   - 같은 URL 입력 시 동일한 결과값 도출
   - 결과값은 주소를 제외하고 8글자 이내로 생성
   

2. DB
    - id, original url, shorten url, date(?)
    - 비용을 최대한 줄여야함
    - 어떤 db 사용할지?
      - [ ] sqlite 사용, ORM vs 쿼리
   

3. 서버
    - API 설계  
      - [ ] domain.com/api/v1/url/id ~ 형태로 api 설계하는게 좋지 않을까?
    - 데드락 문제 발생 가능성 체크
    - http 301 vs 302
    - 중복체크
      - [ ] 중복체크시 길이가 긴 url을 그대로 사용하면 비효율적이므로, md5 해시함수 사용하여 길이 줄인 후 체크


4. 해시 함수
    - 해시값과 1대1 대응을 해야한다. -> 단순 랜덤 생성은 절대 안됨.
    - 인코딩과 디코딩 둘 다 가능해야할듯 싶다.
    - url : 중복 체크를 하기위해 되도록 짧은 해시함수 사용
    - id : base64 vs base62
       - "+", "/", "="가 문자 내부에 있다면 제대로 처리가 안될 가능성이 있기때문에 base62사용
       - base62 사용시 최대 id 62^8 번까지 커버 가능
    - url을 소문자로 강제변환시켜야할지 고려 -> 그냥 입력받는대로 생성하자.
    
        
5. 코드 품질을 높일 수 있는 방법
    - PEP 8
      - [ ] 주석처리 깔끔하게
      - [ ] python docstring 작성하기
    - 각 함수마다 딱 하나의 기능만 할 수 있도록!

