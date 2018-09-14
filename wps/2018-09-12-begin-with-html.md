---
layout: post
title:  "Begin with HTML"
author: "Seongwon Han"
---

## Web을 알기 위해서는 HTML을 알아야 한다

*어디부터 시작을 해야하는지 모른다면 여기부터 시작하자.*  
### HTML?
Hyper Text Markup Language로 "Hyper Text"부분은 서로 전송이 가능하다고 보면 되고 "Markup Language"는 태그(Tag)를 활용하여 구조를 짜는 언어라고 이해하면 된다. 

#### HTML 구조  

- <태그>로 시작하여 </태그>로 끝나는 것을 볼 수 있는데, <html>이라는 태그 안에 있으면 브라우저에서 확인이 가능하다.  
  
~~~
<!DOCTYPE html><html>   <<<html 문서의 시작<head><title>Document</title></head><body><!-- 이 사이에 넣는 내용은 주석이 됩니다 -->  <<<주석</body></html>  <<<html 문서의 끝 
~~~  

#### 태그의 요소와 속성  
~~~
<a href=“http://naver.com”>네이버 홈으로 가기</a><img src=“https://www.google.co.kr/logo.png>
~~~
`<a ...> </a>`는 `a`요소를 가진 태그이고 `href="..."`는 태그의 속성이다

#### 태그구분  
-  `<head>` 는 페이지의 메타데이터 집합
-  `<body>` 는 브라우저에 표시될 내용  
-  HTML이 어떻게 사용되고 있는가를 보기 위해서 [네이버](https://www.naver.com)로 이동 후 `view` > `developer` > `view source`를 통해 확인해본다.  

#### 어차피...
어차피 HTML에 대한 완벽한 이해는 불가능하니, 다 이해되지 않더라도 필요할 때 어디에 있는 자료로 학습을 해야하는지에 대해서 알면 좋다.  

[W3school](https://w3schools.com)에 접속하면 *html*, *CSS* 튜토리얼을 통해 학습이 가능하다.