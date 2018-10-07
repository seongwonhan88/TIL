## 네이버 웹툰 크롤링
### 페이지 넘기면서 데이터 불러오기

![](https://t1.daumcdn.net/thumb/R1280x0/?fname=http://t1.daumcdn.net/brunch/service/user/zIH/image/nLE2lv_EFOsTcnqYVutH9vn6cpc.jpg)

#### pagination 확인의 필요성
특정 웹툰의 에피소드 목록이 일정 분량을 넘어가면 자동으로 pagination 처리가 되기 때문에 1개 페이지만 크롤링을 할 경우 마지막 n 개의 에피소드만 크롤링을 하게 된다. 

![](https://archive.fo/kG3sF/53a2e7fb55fe74ab7d83bbb4db61534e6659693d/scr.png)

따라서 페이지들의 정보가 존재하는지 확인하고, 마지막 페이지까지 따라가서 첫번째 에피소드 까지 끌고오는 작업을 해본다. 크롤링 자체는 별도 포스팅을 할 계획이라 이번 글에서는 pagination을 어떻게 활용하는지 알아본다.  

#### 필요한 library 불러오기
~~~
from bs4 import BeautifulSoup
import requests
~~~
> `requests`(URL 처리) 와 `BautifulSoup`(데이터 파싱)을 import 처리 해준다. 

#### URL REQUEST 
- url 변수에 원하는 페이지를 `request.get`을 통해 할당한다 
- 그리고 `url.text`url의 텍스트 값을 `html`변수에 할당한다.  
- 

~~~
page_num = 1
url = requests.get('https://comic.naver.com/webtoon/list.nhn?titleId=703847&page={page_num}')
html = url.text
~~~
> 먼저 특정 웹툰의 에피소드 목록을 보는 페이지를 긁어온다. list.nhn?뒤부터 GET request를 통해 정보를 얻어오는 것을 볼 수 있다.  

우리가 긁어오는 웹툰의 ID는 `titleID=703847`이고 `&page={page_num}`에서 1번 페이지를 불러온다.  
>사실 `page`의 파라미터를 1을 주던 100을 주던 일치하지 않을 경우 가장 처음이거나 가장 마지막 페이지로 넘겨버린다. 그래서 단순히 page값을 증가시키는 루프를 돌리면 break를 걸 수 없다. 


#### 할당한 내용 파싱하기(parsing)

~~~
...
soup = BeautifulSoup(html, 'lxml') 
paginate = soup.select('div.paginate a')
page = paginate[-1].get('class')
~~~

`soup`에 `html`을할당 한 후 파싱을 하는데  
`html`(에피소드 목록을 가진 페이지)안에서 pagination을 담당하는 태그를 찾아야 한다.  

> FYI, 크롬 개발자 도구를 사용하면 찾기가 편하다.
![](https://i.stack.imgur.com/9STcX.gif)

- pagination 을 담당하는 태그는 `<div class="paginate" .. `라는 태그 아래 `<a ...` 태그를 가지고 있다.  
- `paginate`에는 위의 조건을 가진 태그들을 리스트에 저장한다.  
- `page`에는 마지막 태그의 `<a class="{여기}"`에 할당된 값을 가져온다. 
- 마지막 페이지일 경우, 마지막 태그의 값이 `page`가 되고, 그렇지 않을 경우는 `next`가 값이 된다.  

조금 두서 없이 설명했지만, 로직을 설명하자면  


> GET 요청 시 `page`의 파라미터를 순회하며 `<div>` 안에 속해있는 마지막 `<a>` 의 class 값이 next가 아닐때 까지 페이지를 불러오고 읽으면 된다.  

코드는 아래와 같다.  

~~~
page_num = int(1)

while page[-1] == 'next':
    url = requests.get(f'https://comic.naver.com/webtoon/list.nhn?titleId=703847&page={page_num}')
    html = url.text
    soup = BeautifulSoup(html, 'lxml')
    print('parsing', page_num)
    paginate = soup.select('div.paginate a')
    page = paginate[-1].get('class')
    page_num += 1   
~~~