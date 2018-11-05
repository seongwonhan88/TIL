---
layout: single  
toc : true  
title:  "OAuth: SNS계정으로 로그인하기"  
author: "Seongwon Han"  
tags: oauth2 django  
category: how-to
---

## Social login 과정
### Oauth 전달방식 이해하기

![](https://i.stack.imgur.com/9LOsS.png)

기존에 ID/PW 로그인 방식에서 발생하는 문제들을 해결하고자 제3의 인증기관을 이용해 서비스에 본인 인증을 하는 방식이다. 

#### 인증방식  

1. 소비자가 서비스제공자에게 요청토큰을 요청한다.
2. 서비스제공자가 소비자에게 요청토큰을 발급해준다.
3. 소비자가 사용자를 서비스제공자로 이동시킨다. 여기서 사용자 인증이 수행된다.
4. 서비스제공자가 사용자를 소비자로 이동시킨다.
5. 소비자가 접근토큰을 요청한다.
6. 서비스제공자가 접근토큰을 발급한다.
7. 발급된 접근토큰을 이용하여 소비자에서 사용자 정보에 접근한다.


#### 관련 동영상 
<iframe width="560" height="315" src="https://www.youtube.com/embed/Oy5F9h5JqEU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

### 구글로 로그인하기  
인증방식은 위에서 설명한바와 같지만, 저 인증 과정들을 자동으로 해주는 애플리케이션이 있다.  
장고에 문제없이 잘 설치만 하고나면 구글 뿐만 아니라 Oauth 2.0을 제공하는 많은 서비스들을 활용 할 수 있다.  

구글링을 열심히 하다가 [이 블로그](https://buildenigma.com/blog/integrate-social-login-in-your-django-project-within-minutes/)를 발견하게 되었다.  
삽질전에 열심히 구글을 뒤져서 편리한 방법을 찾는것도 기술인듯.   

상당히 활발하게 개발되는 오픈소스이다. [github 공식 페이지](https://github.com/python-social-auth/social-app-django) 참고  

#### 1. social-auth-app-django 애플리케이션 설치 및 초기 세팅

- PIP로 앱 설치 `pip install social-auth-app-django`  
- `social_django`를 `settings.py`에 추가한다.  
- `python manage.py migrate`로 마이그레이션 실행  
- `settings.py`에 있는 `MIDDLEWARE_CLASSES`에 `social_django.middleware.SocialAuthExceptionMiddleware`를 포함시킨다.   

~~~
AUTHENTICATION_BACKENDS = ( #여기에 인증을 원하는 SNS들을 추가
       'social_core.backends.twitter.TwitterOAuth',

	    'social_core.backends.facebook.FacebookOAuth2',

	    'django.contrib.auth.backends.ModelBackend', << 이거 필수

	    'social_core.backends.google.GoogleOAuth2',
	   )
~~~

- `settings.py`에 `SOCIAL_AUTH_LOGIN_REDIRECT_URL`을 초기화 한다. 

~~~
SOCIAL_AUTH_LOGIN_REDIRECT_URL = localhost(DEBUG=True 일 경우) 
~~~

- `config`에 있는 `urls.py`에 path추가  

~~~
path('',include('social_django.urls'), namespace='social')
~~~

#### 소셜 인증 세팅  
이번 예시에서는 구글 로그인을 할 예정이니 [Google's Developer Console](https://console.developers.google.com/)로 이동하여 API활성화 작업이 필요하다.  

-  Project 를 생성한다.  

![](https://buildenigma.com/media/uploads/2017/06/19/create.png)  


-  Google+ API 활성화를 실행한다.  

![](https://buildenigma.com/media/uploads/2017/06/19/googleapi.png)  

- OAuth2 클라이언트 ID를 생성한다.   

![](https://buildenigma.com/media/uploads/2017/06/19/credentials1.png)

- Web application을 선택  

![](https://buildenigma.com/media/uploads/2017/06/19/createclientid_wXZDnoQ.png)  

- redirect URIs에 `localhost:8000/oauth/complete/google-oauth2/` 입력한다.  

- `settings.py`에 돌아가서 공개키와 비밀키를 입력한다. (하드코딩하지말고 숨겨진 공간에 있는 것을 불러오는 걸로)  

~~~
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = [Your app's client Id]
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET  = [Your app's secret]
~~~  

- 로그인을 받는 인덱스 페이지(html)에 `a`태그를 생성하여 아래와 같이 입력한다.  

~~~
<a class="loginBtn loginBtn--google" href="{% url 'social:begin' 'google-oauth2' %}">Login with Google</a>
~~~  

### 순서대로 잘 따라했는데 안된다면 아래 동영상을 보고 따라해보자.  

<iframe width="560" height="315" src="https://www.youtube.com/embed/6w-Vu2RknsE" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
