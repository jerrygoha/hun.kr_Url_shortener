# Url_shortener

### Preview
<img width="100%" src="https://user-images.githubusercontent.com/48903443/140422113-6411ec34-09b8-4a74-aad0-2aa739c974f0.gif"/>

[영상으로 보기](https://youtu.be/OZXnNHopzME)

### TO-DO
1. URL Shortener
    
2. DB는 어떻게?
    - id, original url, shorten url, date(?)
    - 비용을 최대한 줄여야함
    - 어떤 db 사용할지? -> sqlite
    

3. 서버는 어떻게?        
    - 인코딩된 코드를 db에 저장해두면 좀더 효율적이지 않을까? (-> db접속 vs 내부 function)
    - responce에 바로 redirect 정보 담아 보내기
    - 페이지에서 redirect 코드 실행하기    
    - domain.com/api/v1/url/id ~ 형태로 api 설계하는게 좋지 않을까?
    - 데드락 문제 체크하기
    - redirect시 301 vs 302 어느것을 사용할지 고민해보기


4. 해싱함수
    - 해시값과 1대1 대응을 해야한다. -> 단순 랜덤 생성은 절대 안됨.
    -     
    
        
5. 코드 품질을 높일 수 있는 방법
    - PEP 8 참고
    - 각 함수마다 딱 하나의 기능만 할 수 있도록!
    

6. 기타 아이디어    
        

---

hashing 방법(메모)

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
