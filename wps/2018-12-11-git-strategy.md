---  
layout: single  
toc : true  
author: "Seongwon Han"  
title: "Git: Strategy를 활용한 merge"  
tags: git 
category: how-to 
---  

## Branch의 내용을 살리고 싶을 때  
### Master에서 갈라져 나온 후  
Master에서 Branch를 파서 작업을 진행을 했고, 어떤 이유에서인지 Master보다 내 Branch를 활용하고 싶었다.  

나의 경우 Master에서 migration파일을 지워버리고 Commit을 해버린 바람에 migration 파일이 있는 위치로 돌아가서 branch를 다시 생성했고, 해당 migration을 살리면서 내용들을 적용시키고 싶었다.  

그렇지만 master는 지우거나 대체 할 수 없기 때문에 3-way-swap을 시도해본다.  

1) 나의 branch로 이동한다(checkout)  
2) 현재 나의 branch를 기준으로 merge 시킨다  
> 이럴 경우 내가 살려둔 migration파일들이 지워지지 않으면서 업데이트 된 내용들이 branch에 merge를 시도한다   

3) conflict가 있을 경우 해결하고, commit을 완료한다  
4) master로 이동 후 나의 branch를 삭제한다  

~~~
>>> git checkout my_branch
>>> git merge --strategy=ours master 
>>> git checkout master 
>>> git branch -D my_branch 

~~~

좋은 방법인지는 모르겠으나, 혹시라도 필요할 경우에는 유용하게 쓸 수 있다. 

[merge strategies](https://git-scm.com/docs/merge-strategies)를 참고하여 상황에 적절한 merge를 해보아도 좋을 듯 하다.  