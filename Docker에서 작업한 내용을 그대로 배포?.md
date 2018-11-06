## Docker에서 작업한 내용을 그대로 배포?
### AWS Elastic Beanstalk 활용하기  
![](https://cdn-images-1.medium.com/max/1600/1*bnHhvA0rzKb-ZBw0XE8qJQ.png)



### Docker hub에 Dockerfile.base 업로드(Docker용량 최소화)   
	- Hub에서 올라온 미니멀 이미지에 빌드 
### 설치 변수가 많은 것은 Dockerfile로 관리  
	- 로컬을 받아서는 eb deploy가 되지 않으니 Docker hub에 올려놓은 파일을 FROM에 적용 

### AWS Elastic Beanstalk 
	- cli eb 설치
	- pip install awsebcli # install eb cli mode
	- eb init --profile eb #credential autosetup  
	- 

#### 참고  

- [Elastic Beanstalk으로 Django 배포하기](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html)  
- [Docker  ](https://docs.aws.amazon.com/ko_kr/elasticbeanstalk/latest/dg/create_deploy_docker.html)