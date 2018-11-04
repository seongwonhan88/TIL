---
layout: single  
toc : true  
title:  "AWS: 구조별 분리"  
author: "Seongwon Han"  
tags: aws linux ubuntu 
category: how-to
---

AWS 내에서 역할 분리 

`request -> EC2 > 
Webserver App(Nginx) > request받아서 응답 
WSGI app > (webserver python web app 중개역할)
Python Web application > 동적으로 response 기능`

EC2 서버 컴퓨터 
S3 클라우드 객체 스토리지  
- AWS IAM   
- S3 계정생성 - s3full access권한

RDS 클라우드 데이터베이스 서버 

Docker(운영체제 가상화) 


BOTO3 생성
.aws/config, .aws/credentials 안에 key/secret저장 


