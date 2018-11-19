## Docker에서 작업한 내용을 그대로 배포?


### 참고  

- [Elastic Beanstalk으로 Django 배포하기](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html)  
- [Docker  ](https://docs.aws.amazon.com/ko_kr/elasticbeanstalk/latest/dg/create_deploy_docker.html)

## AWS Elastic Beanstalk 활용하기  

<iframe width="560" height="315" src="https://www.youtube.com/embed/SrwxAScdyT0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe> 

Elastic Beanstalk은 Docker외 다른 Application의 배포를 지원하지만, Docker에서 배포 환경 테스트를 마친 후 실제 배포까지 단계를 최소화 해본다. 

## 준비사항  
- AWS Account(Deployment Environtment)
	- IAM account(Elastic Beanstalk)
	- S3 Bucket
	- RDS Databases
- Docker Hub Account
	- Docker base
- Docker(Test Environment)
	- Python 3.6.7-slim(Debian)
- Django(Application)
	- Python 3.6
	- Pillow(imagefile)
	- Boto3(S3 bucket interface)
	- Dockerfile(EB에서 Dockerfile자동인식->배포)
- Git
	- Commit단위로 배포
- Nginx(웹서버)
- WSGI(웹서버 인터페이스)

## 작업순서
1. Application 준비: 개발할 어플리케이션(Django) 세팅   
1-1. 환경설정: 가상환경에 필요한 파일 준비  
1-2. 모델설정: 유저모델 상속   
1-3. 비밀설정: 비밀폴더 생성, 비밀파일 관리  
1-4. 버전관리: GIT 생성 / GITIGNORE생성    
1-5. 데이터베이스/버킷 연결: AWS S3(S3User설정), RDS 연결(보안그룹 설정)   

	**runserver로 로컬 테스트**

2. Docker 실행   
2-1. Dockerfile 생성  
2-2. Nginx 설치 추가, uWSGI설치 추가  
2-3. Dockerfile base 생성: 배포용량 최소화  
2-4. Docker Hub에 게시: Dockerfile base push   

	**Docker 테스트**

3. EB 실행 
3-1. EB 설치  
3-2. EB 초기화(Dockerfile있는 디렉토리로 이동)  
3-3. IAM 계정 설정 (로컬 시크릿 credential에 적용)   
3-4. EB deploy   

	**EB 테스트**


## 세부내용 

### 1. Application 세팅 
**환경설정**

~~~
pyenv virtualenv 3.6.6 <env_name>
pyenv local <env_name>
pip install --upgrade pip
pip install django django-storages pillow boto3 awsebcli psycopg2-binary 
brew postgresql
~~~

**어플리케이션 설정**

~~~
django-admin startproject config
mv config app 
~~~


**PyCharm 실행** `$ charm .`

**PyCharm interpreter 설정**  
-`/usr/local/var/pyenv/versions/<env_name>/bin/python`  
- Django Support enable  

**모델설정**  

Terminal에서 모델을 만들기 위한 앱 추가

~~~
cd app
./manage.py startapp members
~~~

config.settings.py에 생성한 모델이름 추가

~~~
INSTALLED_APPS = [
	...,
	'members'
]
~~~

members.models.py에 User모델 생성  

~~~
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    img_profile = models.ImageField(
        upload_to='user'
    )
~~~

**비밀설정**

데이터베이스, 스토리지 등 접속을 위해서 인증 키들을 많이 보유하게 된다. 이 때 비밀 키들은 별도 폴더에 저장하여 동적 할당을 해주어 외부에서 접근해도 실제 키를 볼 수 없게 한다.  


Terminal  

~~~
cd .. (project level)
mkdir .secrets
~~~

/.secrets/`secret.json` 생성, config/`settings.py` 에 있는 `SECRET_KEY` 가져옴

secret.json

~~~
{
  "SECRET_KEY":"wd=nm)i0xwbk1krabc=5q#v!7=2ahhsn@u9@-vb_pdzj(c%4)d"
}
~~~

settings.py를 python package로 변경, 아래와 같은 구조로 설정

~~~
├── settings
│   ├── __init__.py
│   ├── base.py
│   ├── dev.py
│   └── production.py
~~~

base.py  

~~~
import json
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = os.path.dirname(BASE_DIR)
SECRET_DIR = os.path.join(ROOT_DIR, '.secrets')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, '.static/')

secrets = json.load(open(os.path.join(SECRET_DIR,'secrets.json')))
SECRET_KEY = secrets['SECRET_KEY']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'members',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True

~~~

dev.py (RDS 생성 후 DATABASE 내용 교체)

~~~
from .base import *
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
WSGI_APPLICATION = 'config.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
~~~

production.py  RDS 생성 후 DATABASE, ALLOWED_HOSTS 내용 교체)

~~~
from .base import *
DEBUG = False
ALLOWED_HOSTS = []
WSGI_APPLICATION = 'config.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
~~~

**.gitignore 생성**  

- [gitignore.io](https://www.gitignore.io/)에 접속하여 git, django, pycharm+all, linux, macos 추가하여 생성   
- 실제 .gitignore파일에 들어간 후 .으로 시작하게될 폴더들도 추가

**버전관리 first commit**  
- 비밀 내용들이 git에 포함되지 않는것을 확인하였으면 `git init`후 first commit을 실행  
- `git add .` 처리 후 `git status`를 입력하여 비밀 디렉토리가 추가되지 않은 것을 꼭 확인  


**IAM 사용자 설정**  
- 콘솔에서 S3에 접속할 사용자 계정 생성 후 ~/.aws/credentials에 등록  

**보안그룹 설정**  
- 해당 IP에서 접속이 가능하도록 보안그룹 설정, 해당 보안그룹은 추후 RDS에 적용  


**AWS에서 RDS 인스턴스 생성, DB 구축하기**  

[AWS Console](https://ap-northeast-2.console.aws.amazon.com/console/home?region=ap-northeast-2)  
- 콘솔에 접속 후 RDS로 이동, 인스턴스 생성에서 PostgreSQL선택  
- 인스턴스명 설정, 마스터 사용자 생성  
- DB이름, Public Access 활성 화 후 생성 
- 보안그룹 설정  
- secret에 DATABSES를 json으로 저장, settings/dev.py 와 settings/production.py에 동적으로 할당  
- manage.py makemigration 후 migrate  
- 생성된 DB에 접속을 원할때는 아래와 같이 접근한다  

~~~
#command line
psql --user=[userid] --host=[host..amazonaws.com] [dbname]  


~~~


**AWS에서 S3 버킷 생성, 스토리지 구축하기** 

Terminal

~~~
ipython
>>> import boto3 
>>> client = boto3.client('s3')
>>> client.create_bucket(
>>> 	Bucket='mybucket',
>>> 	CreateBucketConfiguration={
        'LocationConstraint': 'ap-northeast-2'
    	},
~~~

> Boto3는 ~/.aws/credential 을 자동으로 찾아서 [default]로 적용된곳으로 이동한다.  
> 따라서 여러 계정으로 적용중일 경우에는 실수 하지 않도록 주의!   

### 2. Docker 작업 

#### Docker 설정  
- [docker 홈페이지](https://www.docker.com/)에 가서 Docker를 받아 설치한다.  
- [docker hub](https://hub.docker.com/)에 가입한다.  
Docker hub는 github와 마찬가지로 Docker repository를 생성할 수 있다.  

#### Docker내 Web Application 저장 장소
> 보통 `~/srv/project` 혹은 `~/home/project`에 저장하지만 이번에는 `~/srv/` 안에 저장한다.  

#### 웹서버와 애플리케이션 서버 인터페이스 구축
이 항목은 거의 동시에 설정함에 따라 별도 설명을 추가했다.  
우선 HTTP request들을 처리해줄 nginx를 설정해준다.  

#### nginx 설정
	
ROOT_DIR에 app.nginx 생성 

~~~
# /etc/nginx/sites-available
server {
    # listen on port 80
    listen 80;
    #domain name localhost
    server_name localhost;
    #encoding
    charset utf-8;
    #requiest/response max size
    client_max_body_size 128M;

    #('/' starts) -> responding to all url connection
    location / {
        # uwsgi connection using unix socket
        # "tmp/app.sock" file is used
        uwsgi_pass unix:///tmp/app.sock;
        include uwsgi_params;
    }
    #ip hashing config.
    location /static/ {
        alias /srv/project/.static/;
    }
    location /media/ {
        alias /srv/project/.media/;
    }
}
~~~

`location` 단위로 묶어서 HTTP에서 요청하는 URL 값에 따라 접근 경로를 바꿔서 처리해준다.

ROOT_DIR (`/`)로 접근 할 경우에는 uWSGI로 연결(아래 uWSGI 설정 확인)
  
> 최종 목적은 정적 파일들에 접근하는 요청(request)가 왔을 경우에 Django까지 가지 않고 S3 bucket (`/srv/project/.static/`) 으로 이동할 수 있도록 경로 설정  


#### uWSGI 설정  
nginx 와 Django를 연결해줄 인터페이스. 
uWSGI에 다른 기능들도 있지만 이번 연결에서는 nginx에서 보내주는 데이터 수신을 목표로 한다. 

ROOT_DIR에 ini.uwsgi 생성 

~~~
[uwsgi]
;python application dir(django project)
chdir = /srv/project/app
; application and wgsi connection module
wsgi = config.wsgi.production
;using socket to connect
socket = /tmp/app.sock
; auto delete when uWSGI is finished
vacuum = true
; socket authority change / user change
chown-socket = www-data
~~~

**세부 단계는 아래와 같다.**  
- docker내에 django가 설치된 위치를 설정  
- wsgi 불러오기  
- socket 설정(nginx-uwsgi는 socket으로 통신)  
- 사용 완료되면 삭제  
- socker owner를 www-data로 변경   


### Dockerfile & Dockerfile-base 설정  
- Dockerfile을 만들어 놓으면 기본 Docker에서 웹애플리케이션을 위한 환경설치 명령어들을 입력해놓고 Build를 시작할 수 있다.  
- Dockerfile들을 만들면서 반복적으로 설치되는 명령어들을 모아서 Dockerfile-base를 생성하면 시간을 단축할 수 있는 장점이 있다.      
- 사용량 단위로 과금이 되는 Cloud환경을 사용할 경우 이 점을 꼭 기억하여 효율적으로 활용하는 것이 중요하다.  


Dockerfile 과 Dockerfile-base의 모습은 아래와 같다.  

Dockerfile-base

~~~
FROM python:3.6.7-slim
MAINTAINER owner@myemail.com

#package upgrade
RUN apt-get -y update
RUN apt-get -y dist-upgrade
RUN apt-get -y install gcc nginx supervisor && \
    pip3 install uwsgi && \
    apt -y remove gcc && \
    apt -y autoremove

# copy requirements
# if requirements has not changed, pip3 will not install
COPY requirements_production.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
~~~

Dockerfile(확장자 없음)  

~~~
# docker build -t eb:docker -f Dockerfile .
FROM        owner/eb-docker:base
ENV         DJANGO_SETTINGS_MODULE  config.settings.production

# copy application source code to deployment folder in docker
COPY        ./   /srv/project
WORKDIR     /srv/project

# process commands
WORKDIR     /srv/project/app
RUN         python3 manage.py collectstatic --noinput

# delete default Nginx and copy my link setup
RUN         rm -rf  /etc/nginx/sites-available/* && \
            rm -rf  /etc/nginx/sites-enabled/* && \
            cp -f   /srv/project/.config/app.nginx \
                    /etc/nginx/sites-available/ && \
            ln -sf  /etc/nginx/sites-available/app.nginx \
                    /etc/nginx/sites-enabled/app.nginx

# supervisor설정파일 복사
RUN         cp -f   /srv/project/.config/supervisord.conf \
                    /etc/supervisor/conf.d/

# 80 port open
EXPOSE      80

# supervisor run 
CMD         supervisord -n
~~~

### Docker setup 과정 
- 기본 OS를 받는다. Docker Hub에 가면 이미 빌드가 완료된 Docker들이 존재한다. Django는 Python 3.6을 필요로 하는 OS가 필요하니 해당 OS를 찾아 Build를 한다.  

> 꼭 Docker의 사이즈는 최소화 하는 것이 중요 

- 웹 애플리케이션을 위해서 필요한 기본 설정들을 Docker에 설치한 과정을 Docker-base에 저장
- 이 후 Commit 단위에서 재설치/설정이 필요한 명령어들은 Dockerfile에 저장하여 실제 배포 단위는 Dockerfile이 담당

