---
layout: single  
toc : true  
title:  "WSGI: Web Server Gateway Interface"  
author: "Seongwon Han"  
tags: WSGI, python
category: how-to
---

## WSGI? 


WSGI에 대한 문서는 [PEP3333](https://www.python.org/dev/peps/pep-3333/)에 나와있다.  
 WSGI의 목표는 서버들과 웹 프레임워크/애플리케이션과 상호 관계를 편리하게 연결하는것이 목표이고 웹서버들의 표준 API가 웹 프레임워크(Django, Flask와 같은)들과 연결되어 대화할 수 있도록 정의한다.  
..라고 이야기 하지만 사실 그림으로 그리면 조금 이해하기 편하다. 

### WSGI 개념 
> 구글링을 하면 수없이 많은 이미지들이 존재한다. 그중 알아보기 쉬운 몇가지들을 공유하니 공통점을 찾아보길  

![](https://image.slidesharecdn.com/secretsofawsgimaster-170806022036/95/secrets-of-a-wsgi-master-2-638.jpg?cb=1504852163)
> image from slideshare

![](https://blog.appdynamics.com/wp-content/uploads/2016/05/g5dlafgwtz05_cpptiktuiqbj6isrtjtxvejauutz58vkwtl1je7y2n9bnu1tmf_ofggmhd0xegrn2dlee6en4tpq9x-8kmlgmhgfucb7erjetcdzg9qrbldwgm7gmdyekj5dri5.png)
> image from APPDynamicsBlog  

![](https://i.imgur.com/H9JNiKu.png) 
> image from [초보몽키의 개발공부로그](https://wayhome25.github.io/blog/)

### 개념정리  
1. http 리퀘스트가 들어오면  
2. 웹 서버가 그 리퀘스트를 받고  
2-1. 서버사이드 처리가 필요 없으면 리스폰스를 리턴(static한 웹 서버)  
4. 서버사이드 처리가 필요하면 **wsgi** 미들웨어를 통해 파이썬 어플리케이션으로 리퀘스트 전달  
5. 파이썬 어플리케이션이 리퀘스트를 받아 처리 후 wsgi 미들웨어 - 웹서버를 통해 리스폰스 리턴.

> 자세한 내용 [여기](http://khanrc.tistory.com/entry/WSGI%EB%A1%9C-%EB%B3%B4%EB%8A%94-%EC%9B%B9-%EC%84%9C%EB%B2%84%EC%9D%98-%EA%B0%9C%EB%85%90)참조