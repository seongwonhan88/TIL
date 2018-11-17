---
layout: single  
author: Seongwon Han  
title: "Django: Django Install 1"  
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
pip install --upgrade pip
pip install django~=1.11.0
~~~

이렇게 하면 장고 설치가 끝난다. zsh의 l을 아무리 눌러도 아무 변화가 없어보인다.

### 4. Pycharm interpreter setting  
장고 사용에는 개발도구인 Pycharm 을 사용할 것이다.  
인터프리터 세팅을 가상환경으로 만든 것으로 아래와 같이 설정해줘야한다.(안그러면 command-line에서 실행이 안된다  
`command + ','`를 눌러 세팅을 연 뒤 Project Interpreter를 설정한다. 

![](https://i.stack.imgur.com/JWpB1.png) 

우리는 위에서 가상환경에 pyenv virtualenv를 만들었으니 그 경로를 찾아줘야 가상으로 등록한 파이썬이 돌아간다. **이 작업을 꼭 해주고 다음 작업을 진행해야 한다!**  

위 그림과 같이 아래 화살표를 클릭한 후 Show All 을 누른 뒤 아래 경로를 입력해준다  

~~~
usr/local/var/pyenv/versions/가상환경이름/bin/python
~~~
python 과 python3가 보이겠으나, python을 선택하고 ok!

### 5. Project 만들기  
장고는 framework다. 어떤 프로젝트를 만드는데 필요한 frame(틀)을 제공하는 것이니 장고 설치가 끝나도 프로젝트가 없으니 아무것도 없다.   
아래와 같이 프로젝트를 생성해보자  

~~~
python django-admin.py startproject mysite
~~~
이렇게 하면 현재폴더에 mysite라는 폴더가 하나 설정된 것을 확인할 수 있다.  
다음은 블로그라는 어플리케이션을 만든다  

~~~
python manage.py startapp blog
python manage.py migrate 
~~~
이제 mysite안에 blog 라는 패키지가 생성되고, 파일들이 들어가 있음을 확인 할 수 있다. 
blog 패키지를 migration 하기 위해 `makemigration` 을 아래와 같이 진행한다

~~~
python manage.py makemigrations blog
python manage.py migrate 
~~~

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

장고는 프로젝트 생성과 함께 admin 페이지를 제공하는데 가장 큰 장점 중 하나다.  
이제 주소창에 http://127.0.0.1:8000/admin을 입력하면 아래와 같은 화면이 뜬다.  
![](https://tutorial.djangogirls.org/ko/django_admin/images/login_page2.png)  
> image from DjangoGirlsTutorial

Admin계정을 만들지 않았으니 `createsuperuser`를 이용해 하나 만들자 

~~~
python manage.py createsuperuser
~~~
email, password를 입력한 후 다시 admin page로 돌아와서 login을 하면 아래와 같은 화면이 보인다.  

![](https://docs.djangoproject.com/en/2.1/_images/admin02.png)  

현재까지 완료된 사항을 정리하면 아래와 같다.  
- 가상 환경에 파이썬, 장고 설치  
- `mysite`라는 프로젝트를 생성, local IP(127.0.0.1:8000)로 서브  
- blog 앱/패키지 생성, 블로그 마이그레이션파일 생성(migrate할 준비파일)  
- 마이그레이션 진행  
- admin 계정 생성   

### 6. 모델(Post) 만들기  
현재까지 admin page에는 아무 기능도 없다. 이제 models를 활용해서 post할 수 있는 기능을 만들어본다.  

mysite/settings.py로 이동하여 INSTALLED_APPS에 'blog'를 추가한다.  

~~~

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
]
~~~

그리고 models.py로 이동해서 아래 내용으로 대체한다. (**복붙금지!**)  

~~~
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
~~~

blog 패키지 내 있는 파일을 수정하였으니 다시 makemigration 및 migrate를 진행한다.   

~~~
python manage.py makemigrations blog
python manage.py migrate blog
~~~
migrate 뒤에 대상을 정해주면 선택된 대상만 진행하고, 공백으로 두면 전체를 마이그레이트 하니 주의하자. 

이제 blog에 있는 모델을 데이터베이스에 추가하였으니 blog/admin.py로 이동해서 아래 내용과 같이 바꾼다.  

~~~
from django.contrib import admin
from .models import Post

admin.site.register(Post)
~~~

models.py 파일에서 정의한 Post 모델/클래스를 admin에 등록하는 작업이다.  

다시 admin page로 이동하여 login을 완료하면 아래와 같은 화면으로 바뀌어있을 것이다.  

![](https://tutorial.djangogirls.org/ko/django_admin/images/django_admin3.png)  
> image from DjangoGirlsTutorial  

Post로 들어가서 테스트 파일들을 만들어보자. 


### 참고자료  
여기저기 튜토리얼들을 참고하여 만들엇으니 아래 링크를 따라 들어가서 어떤 원리로 작동하는지 확인해본다.    
- [장고 걸스 튜토리얼: 장고란 무엇인가요?](https://tutorial.djangogirls.org/ko/django/)  
- [장고 공식 튜토리얼](https://docs.djangoproject.com/ko/2.1/intro/tutorial01/)
