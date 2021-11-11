## Url_shortener
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


## TO-DO, Problem
1. URL Shortener (Main)
   - 웹 페이지 입력폼에 URL 입력 시 단축된 결과 출력
   - 브라우저의 주소창에 단축 URL 입력 시 기존 URL로 리다이렉트
   - 같은 URL 입력 시 동일한 결과값 도출
   - 결과값은 주소를 제외하고 8글자 이내로 생성
   
2. DB, 서버
   - ORM vs raw sql
   - shorten url 을 DB에 저장할것인지, 디코딩 함수까지 만들어 그냥 바로 id값을 조회해 original url을 찾는게 나을지 고민해보기.
   - 데드락 문제 발생 가능성 체크
   
3. How to Shorten URL?
   - 해시 함수의 input/output이 1대1로 대응해야함
   - 어떤 알고리즘을 사용할지?

   
## 왜? 그럼 어떻게 하는게 좋을까?
1. URL Shortener
   1. 브라우저 주소창에 단축 URL 입력 시 기존 URL로 리다이렉트
      > http 302 redirection 사용.
   2. 같은 URL 입력 시 동일한 결과값 도출
      > md5 인코딩 후 DB에서 비교, 중복인 경우 기존 id값을 참고하여 결과값 도출
   3. 결과값은 주소를 제외하고 8글자 이내로 생성
      > 튜플의 id값을 base62로 인코딩하여 출력
2. DB, 서버
   1. ORM vs raw sql
      > ORM 사용 
   2. 불필요한 로직 줄이기
      > DB에 접속하는 비용보다  파이썬 인코딩/디코딩 함수 돌리는 비용이 더 저렴하다고 판단되어 shorten url을 db에 저장하지 않기로 결정
   3. 데드락 문제 가능성
      > save() 사용으로 트랜잭션이 겹치지 않도록!
3. How to Shorten URL?
   1. 해시 함수의 input/output이 1대1로 대응해야함
      > output이 일정하지 않다면, 해시값을 무조건 db에 저장해야한다. 따라서 불필요한 비용이 발생하게 된다.
   2. 어떤 알고리즘을 사용할지?
      > original url 중복 체크는 md5를 사용해 긴 url을 줄여 db에서 체크!
      > id값을 shorten url로 사용하기로 결정, 숫자와 영문자를 혼용하므로 base62 사용.
      > id값의 해시값은 따로 db에 저장하지 않으므로 base62는 인코딩과 디코딩 함수 둘다 구현
      
4. 그밖에 고려했던것들
   1. API 설계
      > domain.com/api/v1(버전)/url/id~ 형태로 설계하면 보기에 좋을 것 같다.
   2. 리다이렉트시 301과 302 둘의 차이점?
      > 301 : 한번 들르면 그 다음부터는 서버 들리지 않는다. (영구적으로 이동)<br>302 : 계속 서버에 들림 (일시적인 방법(스크립트 또는 html 태그)으로 이동)<br><br>302를 사용하면 shorten url에 대해 지속적인 모니터링이 가능하지만, 301을 사용하면 첫 요청에 새로운 주소로 아예 옮겼다고 인식하기때문에 모니터링이 힘들것같다.
   3. base62를 써도 될까?
      > shorten url이 최대 8자 이므로 경우의 수는 62^8이 나온다. 이는 약 218조정도 된다. 현재 서비스가 하루 약 1억번씩 사용된다고 쳐도 꽤 오랜기간 무리없이 서비스할 수 있을 듯 싶다.<br><br> 혹시나 218조개 이상의 데이터가 db에 쌓이게 된다면, 최대 9자로 확장하는 등의 조건 변경이 필요할듯싶다. (기존 데이터는 절대 삭제하는 등의 변형을 주어선 안된다!)
   4. md5를 써도 될까?
      > original url을 굳이 md5 알고리즘에 넣고 비교하는 이유가 최대한 비교하는 문자의 길이를 줄이기 위해서이다.<br>해시값 충돌 가능성이 현저히 낮고, 고속 연산이 가능한 알고리즘으로 md5는 적합해보인다!<br>혹시라도 보안적으로 중요하다면 SHA계열 해시 알고리즘도 고려해보자. 