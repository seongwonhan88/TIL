# git으로 협업하기
## central workflow  
중앙에서 master 노드를 가지고 여러명이 복제하여 local에서 사용 후 push 하는 방식  
[여기](https://lhy.kr/git-workflow)를 참고하면 조금 더 이해하기 쉽다.  

## branch   
특정 지점에서 branch 생성하여 프로젝트 내 일부 내용을 수정 가능하다.  
`$ git branch <title>`이라 하면 master와 동일한 노드에 새로운 branch 가 생성되고 새로만든 branch에서 작업을 하기 위해서는 `$ checkout <branch title>`로 이동한 후 작업을 시작하면 된다. 

## workflow와 branch  
서비스가 운영중일 때 master 노드를 직접 바꿀 수 없기 때문에(이러면 서비스가 망가짐) 안정화 된 현재의 스냅샷을 기준으로 branch(복제하여 가지치기)를 한 후 작업을 진행한다. 가지치기는 아래와 같다. 
 
한명이서 작업할 때에는 문제가 되지 않으나 협업을 하기 위해서는 충돌 방지를 배울 필요가 있다. 
