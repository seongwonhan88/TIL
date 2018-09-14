---
layout: post
title:  "Github 에서 Fork 하기"
author: "Seongwon Han"
---

# Fork 개념 이해하기 
협업을 위해서 Master에서 Branch를 열고 작업을 할 수 있지만, 여러명이 동시에 작업을 하게 된다면 Master 관리자는 상당히 어려움을 겪게 될 것이다. 이를 위해 Github에서 Fork를 제공하는데, master repository를 내 개인 공간으로 복사해오는 개념으로 이해하면 될 것같다. 

master repository 우측 상단에 보면 아래와 같은 버튼을 확인할 수 있는데, 저 버튼을 클릭하면 개인 repository에 복사된 것을 확인할 수 있다.  

![fork button](https://git-scm.com/book/en/v2/images/forkbutton.png)  

Fork된 repository의 clone을 로컬에 저장하여 작업 후 내 repository에 push를 하고 다시 내 repository에서 master repository로 pull reuqest를 하면 된다.  

그럼 ***"pull request는 뭐야?"***  

master 관리자가 아닌 이상 master repository에 push할 권한이 없기 때문에 작업을 마친 개인은 master관리자에게 ***'작업을 완료했으니 내가 변경한 내용을 적용시켜달라'*** 는 요청을 하게 되는 것이다. 

|local(my computer)|remote repository(github)|master repository|  
|:----------------:|:-----------------------:|:---------------:|
|   fetch       |          fork     |      "go ahead"        |
|     push   |  pull request  |   accept or decline   |  

여기까지 Fork에 대한 개념을 간단하게 정리해봤다.  
시간이 넉넉치 않아서 이해한 만큼도 제대로 못적었지만, 이해한다기 보다는 먼저 활용해보는 것이 fork의 개념을 아는데에 가장 빠른 것 같다.  

더 자세한 내용을 보기 위해서는 [github 공식 가이드](https://help.github.com/articles/fork-a-repo/)를 참고하자. 