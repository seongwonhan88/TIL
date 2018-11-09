---  
layout: single  
toc : true  
title:  "AWS: ELB http redirect https"  
author: "Seongwon Han"  
tags: aws ELB
category: how-to
---  


## AWS ELB 에서 HTTP로 오는 요청들을 HTTPS로 redirect 처리해주기 (Nginx)

### 인증서가 이미 발행 되었다고 가정한 상태에서

**app.nginx(Nginx 설정 파일)**  
구글링을 하다보면 아래와 같이 설정하라는 글들을 많이 발견 할 것이다. 

~~~
server {
    listen 80;
    server_name _;
    return 301 https://$host$request_uri;
    }
~~~

생각보다 간단하네?   
- 80번 포트 듣고 있다가  
- 내 서버이름으로 접속을 하면   
- 301(redirect) 보내서 https로 처리하면 끝? 

### 그러나 실제로 따라해보면 잘 안되는게 함정  
AWS 환경에서 저런 세팅을 하면 `ERR_TOO_MANY_REDIRECT`라는 에러가 발생한다. 
> 콘솔에서 Load Balancer에는 80번 포트와 433 포트가 열려있으나 둘다 전송을 80으로 하기 때문에 무한루프가 발생하여 위와 같은 에러가 발생한다.     

![](https://docs.aws.amazon.com/ko_kr/elasticloadbalancing/latest/classic/images/DefineLB_Protocols.png) 

AWS를 사용한다면 Elastic Load Balancer가 지원하는 [공식문서](https://aws.amazon.com/ko/premiumsupport/knowledge-center/redirect-http-https-elb/)를 읽어보자  


커스텀 Nginx를 사용하는 경우, 아래와 같이 설정을 해준다.  

~~~
server {
    listen 80;
    listen 433;
    server_name _;
    if ($http_x_forwarded_proto = 'http'){
    	return 301 https://$host$request_uri;
    }
}
~~~

> 80번(http) 뿐만 아니라 433(https)도 들어야 한다. 둘이 붙여쓰면 433이 무시되니 꼭 별도의 줄을 작성하자.  

이래도 잘 모르겠으면 아래 동영상을 보면서 따라해본다.  

<iframe width="560" height="315" src="https://www.youtube.com/embed/hvqZV_50GlQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>