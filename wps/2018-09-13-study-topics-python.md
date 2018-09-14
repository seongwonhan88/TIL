---
layout: post  
title: python install
author: Seongwon Han  
---

# Pyhton 시작하기
## 환경 준비해주기  
- pyenv : python 버전관리 라이브러리, 충돌방지 역할
- virtualenv: 개발환경을 가상환경으로 분리. 프로젝트별로 가상환경 하나씩
- pyenv-virtualenv 

###pyenv 및 pyenv-virtualenv 설치 
~~~  
$ brew install pyenv
$ brew install pyenv-virtualenv  
~~~
를 설치한 후 `vi ~./zshrc`로 들어가서 아래 내용을 추가한다   
> 나의 환경은 mac임에 따라 linux환경은 방법이 다르다. 

~~~  
export PYENV_ROOT=/usr/local/var/pyenv
if which pyenv > /dev/null; then eval "$(pyenv init -)"; fi
if which pyenv-virtualenv-init > /dev/null; then eval "$(pyenv virtualenv-init -)"; fi
~~~  

zshell 환경준비를 위해  
`$ brew install realine zx ` 유틸리티 설치.  
pyenv 에서 필요한 버전으로 python 설치   

~~~  
$ pyenv install 3.6.6
~~~

### Python 설치가 완료되면 프로젝트를 위한 가상환경 만들기  
프로젝트 별로 사용하는 파이썬 버전/가상환경이 따로 존재한다  
pyenv과 관리하는 가상환경 root 에 프로그램들이 설치가 됨에 따라 가상환경 관리를 해주면 된다. 잘 이해 안되지만 아래 내용을 따라가자

`$ pyenv virtualenv 3.6.6 fc-python` 명령어를 프로젝트 진행하는 폴더에 입력하면 가상환경 세팅을 하게 된다.  

~~~
Looking in links: /var/folders/93/qvh01rlj75x9jrrcst13kff80000gn/T/tmpm7vsdj66
Requirement already satisfied: setuptools in /usr/local/var/pyenv/versions/3.6.6/envs/fc-python/lib/python3.6/site-packages (39.0.1)
Requirement already satisfied: pip in /usr/local/var/pyenv/versions/3.6.6/envs/fc-python/lib/python3.6/site-packages (10.0.1)
~~~
세팅이 완료되면 pyenv가 어디에 있는지 확인해보고 fc-python이라고 명시한 가상환경이 존재하는지 확인해본다
`$ echo $PYENV_ROOT`를 입력하여 어디에 설치되어있는지 본다.  

~~~
▶ echo $PYENV_ROOT
/usr/local/var/pyenv
~~~
내 컴퓨터에는 아래 환경에 설치가 되어있다.


###ipython  
**ipython은 가상환경 내에서 설치한다 pyenv 안에서 pip을 사용한다.**
`$ pip install ipython`을 입력하면 가상환경에 ipython 설치된다.   

`$ pip install notebook`을 통해 notebook 설치한다.  
설치 후 터미널에 `$ jupyter notebook`을 입력하면 새로운 브라우저가 열린다 