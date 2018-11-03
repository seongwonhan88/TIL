---
layout: single  
toc : true  
title:  "Django: User Model"  
author: "Seongwon Han"  
tags: python django 
category: how-to
---

## Django Custom User모델 적용(안좋은사례)  
### 이미 auth.User가 사용중인데 custom필드를 추가하고 싶을때  
가능하면 비추하지만 굳이 연습삼아 해야겠다 하면 아래와 같은 방법을 적용 

1. custom User가 적용될 모델을 새로 생성한다.  
2. User는 AbstractUser를 상속 
3. settings.py에 `AUTH_USER_MODEL = app_name.User` 등록 
3. 기존 Migration 파일 삭제 
4. DB삭제 (뜨악)  
5. 새로 makemigration 
6. migrate 

**DB 를 날리는 작업을 진행하기 싫다면(혹은 불가피하게 날릴 수 없다면) OneToOne 관계로 User모델을 새로 만들수 있다.**  

- Customer User에 대해서는 [공식문서](https://docs.djangoproject.com/ko/2.1/topics/auth/customizing/#specifying-a-custom-user-model)를 읽어본다  
- 만에 하나 유저 모델에 필드를 추가할 경우를 고려하여, AbstractUser를 상속받는 기본 Custom User모델을 생성해놓고 시작하는 것이 좋다.
