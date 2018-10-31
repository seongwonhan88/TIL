---
layout: single  
toc : true  
title:  "AWS: Ubuntu 배포준비"  
author: "Seongwon Han"  
tags: aws linux ubuntu 
category: how-to
---

## AWS EC2(Ubuntu) 인스턴스 설치 후 배포준비
### SSH 터미널 접속 

### access via default username  
**`EC2 terminal`**  

~~~
# system 기본 업데이트
sudo apt-get update
# 의존성 검사에 따른 업데이트(뭔가 나오면 엔터로 진행 > 세부내용은 리눅스 공부가 필요)
sudo apt-get dist-upgrade  
#zsh설치
sudo apt-get install zsh
sudo curl -L http://install.ohmyz.sh | sh
#zsh 기본 디렉토리 변경
sudo chsh ubuntu -s /usr/bin/zsh 
# python, python3-pip 설치
sudo apt-get install python3-pip 
# 의존성 파일 자동 삭제 
sudo apt autoremove 
~~~

### locale setup 
**`EC2 terminal`**  
**`sudo vi /etc/default/locale`**

기존에 있는 내용을 삭제 후 추가할 내용
>~~~
LC_CTYPE="en_US.UTF-8"
LC_ALL="en_US.UTF-8"
LANG="en_US.UTF-8"
~~~

일반 배포 파일들은 `/home/<username>/`에 저장


### 경로설정(PATH)  
**`vi ~/.zshrc`** 

> pip3 설치 위치에 따라 경로가 바뀔 수 있다.  

나의 경로는 아래와 같다(아마 대부분 아래와 같을 것으로 예상). 아래 내용을 `vi ~/.zshrc` 에 추가해준다.  
> `export PATH=~/.local/bin:$PATH`

#### 위 경로가 아닐 경우...
pip3설치가 어디 되어있는지 확인하기 위해서 아래와 같은 command를 제공

> `sudo find / -xdev 2>/dev/null -name "<찾고자 하는 파일명>"`  

특정 실행 명령어(아래의 경우 `django-admin`를 알고 있을 경우 아래와 같은 방법을 사용해도 된다.   

> `sudo find / -name 'django-admin'`


### 보안그룹 생성
**`AWS dashboard`**  
AWS 인스턴스 기본 설정은 22번 포트만 열기 때문에 별도로 필요한 포트는 직접 보안그룹에 추가해줘야한다.  

기본 
> EC2 보안그룹 22번 포트

추가  
> 사용자 지정 port 8000 open(예시) 


### SCP를 통해 내용 복제하기
**`local terminal`**

Local에 있는 내용들을 Cloud로 복제시키고자 할 때 PEM키 제공을 통해 진행. 
아래의 command형식을 따른다.   

> `scp -i <pem 파일 경로> -r <로컬파일/폴더 경로> <ec2인스턴스계정>@<ec2도메인>:<복사위치>`

예시 
> ~~~
scp -i ~ myinstance.pem -r ~/projects/deploy/ec2-deploy ubuntu@ec2.ap-northeast-2.compute.amazonaws.com:/home/ubuntu
~~~
