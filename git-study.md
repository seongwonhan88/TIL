# Git 이해하기
## 버전관리 체계 
Git 을 사용하면 버전관리 및 백업이 수월하다. Git의 개념을 이해하고 Github을 활용한 버전 관리 방법을 알아본다  

## git 설치하기
#### installing via brew
커맨드 창에 `$ brew install git `을 입력하여 설치한다(mac os 기준)  
## git documentation  
자세한 내용은 [git documentation](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository) 가이드 및 튜토리얼을 참고하자. 아래에는 간단하게 내가 지정했던 방법만 작성하였다.  
### git directory 지정  
어디서 git을 활용한 버전관리를 할 것인지 지정을 해야한다. 그 말인 즉슨 프로젝트를 진행하는 디렉터리에 git을 활용해야 한다는 점인데 방법은 매우 간단하다.   
git 이 설치되어 있으면 새로 열게 될 프로젝트 디렉터리에 git 을 활성화 시키면 되는데 방법은 아래와 같다  

~~~
$ pwd
$ /Users/seongwon/projects/git 
//내가 사용한 프로젝트 디렉터리
~~~
위와 같이 디렉터리 선택 후
`$ git init`을 입력하면 "git"이라는 꼬리표가 터미널에 따라다닌다.  

## git의 버전관리 이해  
git은 총 4단계의 단계를 활용하여 버전 관리를 하는데 이는 아래와 같다  

| unstaged | unmodified | modified | staged |
|:--------:|:----------:|:--------:|:------:|
|최초 파일생성|아직 변경 안됨|무언가 변화|스테이지 처리완료|

- unstaged : 최초에 파일이 디렉터리에 생성되거나 버전관리에 들어갈 때의 상태다. 아직 git으로 관리되고 있있지 않음 
- unmodified : git으로 관리되고 있는 파일이지만 아무 내용도 변경되지 않은 상태.
- modified : 무언가 변화가 있으며, git으로 관리를 하기 위한 준비상태
- staged : git snapshot 찍힌 상태로 원본 복구가 가능. 

자세한 내용은 언급했던 documentation을 참고하는 것이 좋다.  
**꼭 알고 넘어가야 할 것은 git은 스냅샷을 찍는 기능이 있어 일정 스테이지로 돌아가는 것이 매우 수월하다.**

## git remote 저장소 github
커맨드 창에 `$ git remote`를 입력하면 local 말고 원격에 저장해놓은 장소가 있는지 볼 수 있다. github에 저장을 할 것이라면 repository를 생성한 후 프로젝트와 연결시키면 된다.  
`$ git remote add <url>`을 통해서 원격 저장소와 연결이 가능하다. 
`push`,`pull`,`fetch`를 통해서 local에 저장된 프로젝트와 동기화가 가능하다. 

## 처음 thread 는 master

branch out 하기 전까지는 master thread 라고 이해하면 된다. remote저장소와 진행하는 작업이 `pull`,`push`,`fetch`이건간에 상관없이 저장소 별명(대부분 처음할 때는 origin)과 master를 기억하고 아래와 같은 입력을 통해 동기화를 진행한다 

~~~
$ git pull origin master 
# remote 저장소에 있는 모든 자료들을 가져와서 local보다 진도가 많이 나가 있으면 저장하고 동기화

$ git push origin master
# local에 있는 자료를 remote 에 있는 저장소로 동기화. branch 를 만들어가 pull request를 해야할 경우도 있음

$ git fetch origin master
# remote 와 local 비교. 동기화를 위한 추가 merge가 필요하다
~~~
