## 장고 블로그  
장고걸스 튜토리얼을 통해 블로그를 만들면서 기능들을 확인한다.  

### MVC 혹은 Django MTV 에 대한 이해
Django는 MVC 패턴을 활용한다. MVC 패턴은 소프트웨어 디자인 패턴 중 하나로
Model - View - Controller 세 가지로 구분되며, 장고에서는 Model - Template - View 라 불린다. 
장고에서 왜 이렇게 부르기로 했는지 궁금하다면 [장고 FAQ](https://docs.djangoproject.com/ko/2.1/faq/general/)에 나와 있다.  

![](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/MVC-Process.svg/400px-MVC-Process.svg.png)
> image from wikipedia MVC 

### 1. views.py에 post_list 클래스 만들기  
views.py 는 browser에서 보이게 될 내용들에 대한 클래스들을 만들게 된다. 이제 post_list라는 클래스를 만들어서 리스트가 보이게 해보자.   

### 1-1 urls.py에 페이지 지정하기  
예전에는 정적 페이지들에 index.html들을 하나씩 다 만들어주었지만, 장고에서는 url패턴을 읽는 정규표현식과 템플릿 언어를 사용하여 동적으로 주소를 할당할 것이다.  

- url 패턴: blog/urls.py를 열면 아래와 같은 내용이 있다. 

~~~
urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
~~~  
`startapp blog`를 실행하면서 admin site가 생성되었고 자동으로 따라온 내용이다.  
> home다음으로 `admin/`이 오면 `admin.site.urls`를 반환하라 

이제 우리는 다음과 같은 내용을 패턴으로 만들고 싶다.  
> home다음으로 아무것도 없으면 `views.post_list`를 반환하라 

~~~
from blog import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.post_list, name=post-list
]
~~~  

우리는 blog라는 패키지 안에 views.py라는 것이 생성하였고, 내장함수가 아닌이상 `import` 작업을 반드시 해줘야 정상적으로 작동한다. 

### 1-2 views.py에 post_list 선언하기  
blog/views.py를 열어서 post_list라는 함수를 생성한다.  

~~~
from django.shortcuts import render
from .models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/post_list.html', context)
~~~

> 이제 post_list함수가 request를 받아 호출받게되면 `blog/post_list.html`에 context를 적용하여 표시하게 된다. 

### 1-3 template 관리에 대한 고찰  
장고에서 정적으로 사용될 템플릿들은 어떻게 관리하는 것이 좋을까?  
여기에 두 가지 시나리오를 고려해두자.  

> **내가 만든 패키지들이 항상 원래 만들었던 위치에 있지 않을 수 있다.**  
> **내용을 변경했을 때 적용이 용이해야 한다.**  

장고걸스튜토리얼은 blog 패키지 않에 직접 `post_list.html`을 생성하여 관리하라고 하지만, 패키지 사이즈가 블로그 수준을 넘어 커질 경우에는 이렇게 하면 각 페이지들을 찾고 관리하는 일이 쉽지 않을것이 분명하다.  
그래서 templates라는 패키지를 하나 더 만들어 그 안에 blog라는 폴더를 만들어서 그 안에 `post_list.html`을 관리하고, 만약에 blog 패키지를 다른곳으로 이동시킬 경우 template/blog도 함께 움직이게 하겠다.  

그래서 새로 만들게 될 post_list.html은 아래와 같은 곳에 위치하게 된다.  

~~~
app/
	blog/
	config/
		settings.py
	templates/
		blog/
			post_list.html
~~~

훌륭하게도 장고에서는 위와 같이 템플릿들을 관리하는 폴더들의 경로를 자동으로 잡아준다. 
settings.py에 가보면 아래와 같이 base directory를 잡아주는 변수를 볼 수 있다. 

~~~
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
~~~

가장 안쪽에 있는 괄호부터 해석하는데 내용은 다음과 같다.    
- `os.path.abspath(__file__)` : 현재의 절대경로  
- `os.path.dirname(dir)` : dir의 상위 경로  
- `os.path.join(dir)` : dir 의 하위경로

> BASE_DIR이 가리키고 있는 경로는, `상위경로(상위경로(절대경로 settings.py)` 이기 때문에 `APP/`이다. 위에 settings.py가 있는 위치 참조.

BASE_DIR을 기준으로 teplates가 있는 위치를 `TEMPLATES_DIR`로 지정하면 아래와 같다.   

~~~
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
~~~
그리고 아래로 내려오다 보면 아래와 같은 내용을 발견 할 수 있다.  
`'DIRS'`에 `TEMPLATES_DIR`을 넣어주면 template에 입력된 파일들은 이 경로를 통해서 잡아주게 된다. 

~~~
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #Django가 template 을 로드할 경로 목록
        'DIRS': [
            TEMPLATES_DIR 
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
~~~

### 1-4 post_list.html 에 템플릿 언어 적용하기  
`post_list.html`의 목적은 생성한 post들의 목록을 보여주는 일이다. 하나부터 열 까지 모든 목록을 직접 HTML로 작성을 하는것이 현실적으로 불가능 한 일이니 장고에서는 자체 템플릿 언어를 사용해서 동적 데이터들을 HTML 내에 할당 할 수 있도록 하게 해준다.  

`templates/blog/post_list.html`을 열고 아래와 같이 세팅을 하자. Pycharm에서도 Emmet과 비슷한 기능을 제공하여 `[tab]`을 누르면 자동 완성이 된다. 

~~~
# html:5 [tab] 을 누르면 아래 양식이 자동완성된다. 
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>

</body>
</html>
~~~ 

이제 실제로 템플릿이 어떻게 적용되는지 간단한 루프를 적용해서 원하는 내용을 찾아보도록 하겠다.  
아래 내용을 `<body>` 태그에 추가해보고 `runserver`를 실행해보자. 
> {% for post in posts %}   
> 	{{ post.title }}   
>  {{ post.author }}  
> {% endfor %}

**아래와 같이 admin에 접속했을 때 post한 내용들이 모두 다 출력이 되면 된다.**

![](https://tutorial.djangogirls.org/ko/html/images/step6.png)  
> image from Django Girls Tutorial

**다음 장에서는 bootstrap을 사용해서 CSS 적용하는 내용을 알아본다.**