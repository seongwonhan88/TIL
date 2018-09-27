---
layout: single  
author: Seongwon Han  
title: "Django: Django Install"  
tags: python django  
category: how-to  
---  

## 묻지마 장고 설치하기 
Django Girls Tutorial을 따라하면서 설치를 해본다.  
이해하려하면 어차피 바로 하기 어려우니 일단 따라하면서 배울 것을 추천.  
[장고걸스 튜토리얼](https://tutorial.djangogirls.org/ko/installation/) 을 참고하여도 좋고, 아니면 아래 방법을 활용해도 좋다.

### 1. 장고 설치 경로설정  
나는 home directory 밑에 project라는 연습 폴더가 있다. project아래에 django라는 폴더를 만들고 Djangogirls-tutorial-practice를 만들어 실행할 계획이다. 

~~~
mkdir django
mkdir djangogirls-tutorial-practice
~~~

### 2. 장고 설치전 환경설정  
- virtualenv를 통한 가상환경 설정  
Pyenv가 설치되어 있으리라 믿고, 아니면 [파이썬 설치하기](https://seongwonhan88.github.io/language/python-install/) 포스트를 참조하자

~~~
pyenv virtualenv 3.6.6 fc-djangogirls-tutorial
pyenv local fc-djangogirls-tutorial
~~~
- git 설정  
이것도 설치 되어 있으리라 믿고, 아니면 [git 설치하기](https://git-scm.com/book/en/v1/Getting-Started-Installing-Git) 를 참조하자  

~~~
git init
~~~
해당 폴더(/djangogirls-tutorial-practice)에 들어와서 위와 같이 git 초기화를 한다.  

### 3. pip으로 장고 설치  
파이썬과 git이 준비가 되었으면 이제 pip을 통해 장고를 설치한다. 

~~~
pip install django~=1.11.0
~~~

이렇게 하면 장고 설치가 끝난다. zsh의 l을 아무리 눌러도 아무 변화가 없어보인다.

### 4. Project 만들기  
장고는 framework다. 어떤 프로젝트를 만드는데 필요한 frame(틀)을 제공하는 것이니 장고 설치가 끝나도 프로젝트가 없으니 아무것도 없다.   
아래와 같이 프로젝트를 생성해보자  

~~~
python django-admin.py startproject mysite
~~~
이렇게 하면 현재폴더에 mysite라는 폴더가 하나 설정된 것을 확인할 수 있다.  
그리고 아래와 같이 서비스를 시작해보자  

~~~
cd mysite #mysite폴더로 이동
python manage.py runserver
~~~
그러면 이런 문구가 나온다  

~~~
Performing system checks...

System check identified no issues (0 silenced).

You have 13 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.

September 27, 2018 - 12:09:16
Django version 1.11.15, using settings 'blog.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
~~~

브라우저에서 `http://127.0.0.1:8000/`를 입력하면 아래와 같은 페이지가 보인다.  
 
![](https://tutorial.djangogirls.org/ko/django_start_project/images/it_worked2.png)
>image from Django Girls Tutorial

현재까지 완료된 사항을 정리하면 아래와 같다.  
- 가상 환경에 파이썬, 장고 설치  
- `mysite`라는 프로젝트를 생성, local IP(127.0.0.1:8000)로 서브

### 5. 블로그 만들기  
블로그를 만들면서 장고에 있는 기능들을 알아보자  








### 참고자료  
설치만 하면 뭐하겠는가... 장고라는 웹 프레임워크를 알아야 하니 아래 아래 문서를 읽자.  
- [장고 걸스 튜토리얼: 장고란 무엇인가요?](https://tutorial.djangogirls.org/ko/django/)  
- [장고 공식 튜토리얼](https://docs.djangoproject.com/ko/2.1/intro/tutorial01/)
