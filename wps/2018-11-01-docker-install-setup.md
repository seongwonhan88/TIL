---
layout: single  
toc : true  
title:  "Docker: Docker로 가상환경 설치-실행 해보기"  
author: "Seongwon Han"  
tags: docker linux ubuntu 
category: how-to
---

## Docker 활용하기 
Docker에 개념은 [여기](https://subicura.com/2017/02/10/docker-guide-for-beginners-create-image-and-deploy.html)글을 참고하여 이해하기로 하고, 컨테이너 생성에서 이미지 빌드까지 작업을 따라한다.  

### Docker 설치 
[https://www.docker.com](https://www.docker.com/get-started)으로 가서 로컬 운영체제에 맞는 내용을 설치한다.  
![](https://docs.docker.com/docker-for-mac/images/docker-app-drag.png)
> 맥이라면 dmg패키지 받아서 설치하면 이렇게 된다.  

### 터미널에서 Docker 실행하기 
정상적으로 설치가 되었는지 터미널에 `docker version`을 입력하여 확인한다. 
   
#### 운영체제 이미지 설치하기  
`docker run ubuntu:18.04`(내가 원하는 배포 가상환경)을 실행한다. 처음에는 깔려있지 않아서 아마 아래와 같은 메시지가 출력될 것이다.  

~~~
$ docker run ubuntu:18.04

Unable to find image 'ubuntu:18.04' locally
18.04: Pulling from library/ubuntu
...
~~~

현재 로컬에서 해당 이미지를 찾을 수 없어 설치파일을 가져오는 것이니, 기다리면 자동으로 이미지가 설치된다.  

이미지 설치가 완료되었는지 확인해보자.  

~~~
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
ubuntu              18.04               ea4c82dcd15a        13 days ago         85.8MB
~~~

#### EC2 환경과 동일한 환경 만들기 
Docker를 쓰는 목적 자체가 실제 배포 환경과 동일한 테스트 환경을 **엄청빠르고 편리한** 방법으로 생성하는 것이기 때문에 배포환경과 동일하게 세팅을 해줘야 한다.  

AWS EC2와 동일한 환경을 만들기 위해서 로컬 개발 폴더로 이동하여 `Dockerfiles`를 생성해준다.  
> PyCharm Pro를 사용하면 알아서 Dockerfile을 인식해준다.   

ec2-deploy라는 폴더(예시)에 장고 개발환경이 깔려있다면  
그 안에 생성하면 된다.  

이제 이 파일안에 앞으로 입력하게 될 내용들을 하나하나 복사하면 된다. 

**`Dockerfile`은 가상환경의 `requirements.txt`와 비슷한 개념으로 이해하면 된다.** 

#### 환경을 하나씩 맞춰보기  
각 프로젝트의 배포 환경마다 다르겠으나 대략 예시는 아래와 같다.  

터미널에서 Docker로 가상환경 실행

~~~
docker run --rm -it ubuntu:18.04
~~~
이제 터미널은 방금 생성한 ubuntu 환경이 된다.  

**터미널** | 업데이트 실행 : `apt-get update`  
> **`Dockerfile`** 실행문 추가 : `RUN apt-get update`  
  
**터미널** | 읜존성 파일 업그레이드 실행 : `apt-get dist-upgrade`  
> **`Dockerfile`** 실행문 추가 : `RUN apt-get dist-upgrade`   

**터미널** | 파이썬 및 pip 설치 : `apt-get install python3-pip`  
> **`Dockerfile`** 실행문 추가 : `RUN apt-get install python3-pip`   

#### Docker build작업 시 개발파일 가상환경에 복사하기 

**터미널** | 파이썬 및 pip 설치 : `apt-get install python3-pip`  

> **`Dockerfile`** 실행문 추가 : `COPY . /srv/project/`
> **`Dockerfile`** 실행문 추가 : `WORKDIR /srv/project/`
> **`Dockerfile`** 실행문 추가 : `RUN pip3 install -r requirements.txt`

#### Docker 에서 배포작업 실행  
> **`Dockerfile`** 실행문 추가 : `WORKDIR /srv/project/app`
> **`Dockerfile`** 실행문 추가 : `RUN python3 manage.py runserver 0:8000`

### Docker build하기  
Docker로 가상환경을 만들기에 필요한 준비가 다 되었으면 대략 아래와 같은 `Dockerfile`이 준비가 되어있을 것이다.  

~~~
FROM ubuntu:18.04						<-- 기반 컨테이너
MAINTAINER seongwonhan88@gmail.com	

RUN apt-get -y update
RUN apt-get -y dist-upgrade
RUN apt-get -y install python3-pip

COPY . /srv/project/
WORKDIR /srv/project/
RUN pip3 install -r requirements.txt

WORKDIR /srv/project/ec2-deploy/app/
CMD python3 manage.py runserver 0:8000
~~~

#### docker build command   

`terminal`
~~~
$ docker build -t ec2-deploy -f Dockerfile .
'ec2-deploy'라는 태그의 docker를 만들면서 여기있는(.) Dockerfile에 있는 실행문을 실행해라.   
~~~


### 잘 돌아가나? 
아래 명령어를 터미널에서 실행시킨 후  
~~~
$ docker run --rm -it -p 7000:8000 ec2-deploy
~~~  

브라우저에서 'localhost:8000'으로 접속해서 잘 되는지 확인해보자  
