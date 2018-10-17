---
layout: single  
toc : true  
title:  "Django: Model 이해하기 3"  
author: "Seongwon Han"  
tags: python django  
category: language
---

### 다른 파일에 있는 모델과 관계맺기
다른 애플리케이션에 존재하는 모델들을 현재 활용하는 모델에 연결 시킬 수 있다. 이를 활용하기 위해서 파일의 상단에 어디로부터 가져오는지, 그리고 어떤 모델 클래스를 가져오는지 입력한다. 

~~~
from django.db import models 
from georaphy.models import ZipCode 	#여기서 불러올 경로 설정

class Restaurant(models.Model):
	# ..
	zip_code = models.ForeignKey(
		ZipCode,						# 그리고 불러올 모델 표시
		on_delete=model.SET_NULL,
		blank=True,
		null=True,
		)
~~~

### Meta 옵션   
Metadata를 Meta 클래스를 활용하여 지정할 수 있다.  

~~~
from django.db import models
class Ox(models.Model):
	horn_length = models.IntegerField()
	
	class Meta:
		ordering = ["horn_length"]		#column 명 horn_length 기준으로 정렬
		verbose_name_plural = "oxen" 
~~~

모델의 metadata는 필드가 아닌 모든것을 말한다. `ordering`(정렬), `db_table`(테이블 이름), `verbose_name`(사용자가 읽는 필드이름), `verbose_name_plural`(필드이름 복수화` 등이 이와 같다. `class Meta` 모델은 개발자 기호에 따른 것이지 의무는 아니다.  

### 모델 속성  
#### 객체(objects)  
모델에 가장중요한 속성은 [Manager](https://docs.djangoproject.com/en/2.1/topics/db/managers/#django.db.models.Manager)다. 매니저는 데이터베이스 쿼리 실행이 장고에서 돌아갈 수 있도록 하는 인터페이스 이며, 인스턴스가 데이터베이스로부터 정보를 획득할 수있도록 하는 역할을 담당한다. 커스텀 Manager가 정의되어 있지 않으면 디폴트는 [objects](https://docs.djangoproject.com/en/2.1/ref/models/class/#django.db.models.Model.objects)다. 
> **매니저는 모델 클래스를 통해서만 접근이 가능하며 모델 객체에서는 접근이 허용되지 않는다. **


### 모델 메서드  
모델의 커스텀 메서드는 'row-level'(행단)기능을 객체에 정의한다. 이에 반해  Manager 메서드는 테이블 전체에 대한 작업을 의도하기 때문에 모델 메서드들을 특정 모델 인스턴스에서 작동할 수 있어야 한다.  
**모델이라는 개념안에 비즈니스 구조를 유지하도록 하는 중요한 기술**  
예를 들어 아래 모델은 몇가지 커스텀 메서드를 가지고 있다.  

~~~
from django.db import models

class Person(models.Model):
	first_name=models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	birth_date = models.DateField()
	
	def baby_boomer_status(self):
		# 출생 연도에 따라 베이비붐 세대인지 아닌지 결과를 반환한다. 
		import datetime 
		if self.birth_date < datetime.date(1945, 81):
			return "pre-boomer" 
		elif self.birth_date < datetime.date(1965, 1,1):
			return "baby-boomer"
		else:
			return "post-boomer"
	
	@property
	def full_name(self):
		# Person의 이름 전체를 반환한다.  
		return f'{self.first_name}, {self.last_name}'
~~~

위 예제의 마지막에 사용된 것은 [property](https://docs.djangoproject.com/en/2.1/glossary/#term-property)이다.  
[모델 인스턴스 참조(model instance reference)](https://docs.djangoproject.com/en/2.1/ref/models/instances/)는 [모델에 자동으로 부여되는 메서드의 리스트(methods automatically given to each model)](https://docs.djangoproject.com/en/2.1/ref/models/instances/#model-instance-methods)을 제공한다.  
대부분의 메서드는 override가 가능하지만 아래 두 가지는 반드시 필요할 것이다.  

####  [`__str__()`](https://docs.djangoproject.com/en/2.1/ref/models/instances/#django.db.models.Model.__str__)  
파이썬의 매직메서드로 메서드를 대표하는 string값을 돌려준다. 하지 말아야 할 이유가 없다면 반드시 선언하여 정의해준다.  


#### [`__get_absolute_url()`](https://docs.djangoproject.com/en/2.1/ref/models/instances/#django.db.models.Model.get_absolute_url)  
이 메서드는 장고가 객체를 위해 URL을 계산하게 해준다. admin 인터페이스에서 사용하며 장고가  객체를 위해 URL을 필요로 할때 사용된다.  

### 사전 정의된 모델 메서드 Override  
데이터베이스의 행동을 조작하기 위해 모델 메서드를 커스텀화 하려 할 상황이 생긴다. `save()`와 `delete()`를 보편적으로 조작하게 될 것이다.  

`save()`를 커스텀 한다 하자.  

~~~  
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def save(self, *args, **kwargs):
        do_something() 						# 무언가 커스텀 작업을 하고
        super().save(*args, **kwargs)  	# 진짜 save()메서드 호출 한 후
        do_something_else() 				# 또 다른 커스텀 작업을 한다.  
~~~
 
아니면 실제로 `save()`가 호출되는 것을 제어할 수 있다.  
 
~~~
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def save(self, *args, **kwargs):		
        if self.name == "여기에 조건":		# 조건을걸고
            return "다른 행동"				# 다른 행동을 하거나 
        else:
            super().save(*args, **kwargs)  # 진짜 save()를 호출
~~~  

이 때 슈퍼 클래스 메서드 `super().save(*args, **kwargs)`를 호출하는 것을 기억해야 한다. 

### 모델 상속  
장고의 모델 상속은 파이썬 클래스 상속과 거의 유사하다. 하지만 기본 모델(base model)은 `django.db.models.Model`을 가져야한다.  

> 부모가 되는 모델이 자신의 형태를 가지는지 안가지는지(DB에 테이블이 존재하는지 여부)를 결정하는 것이 모델 상속에서 가장 중요하다.  

장고에는 3가지 상속 유형이 존재한다.  
1. 추상 모델: 많은 테이블에서 공통적으로 사용되는 필드를 추상화 하여 가진다. 이 경우 부모 모델은 실제 DB에 테이블이 존재하지 않고 상속받은 자식 테이블에 필드가 할당된다.  
2. 멀티 테이블: 기존에 존재하던 모델에서 서브클래싱(상속받는)경우 부모와 자식 모두 각각 DB테이블을 가지는 상속 형태.  
3. 프록시 모델: 마지막으로 실제 모델 필드들을 변경하지 않고(부모만 DB테이블 존재), 모델의 파이썬 수준 동작만 수정하려는 경우에 사용하는 상속 형태.  

#### 추상 모델  
추상모델은 해당 모델의 필드가 많은 필드들에서 공통적으로 쓰일때 매우 유용하다. `Meta`에서  `abstract = True`로 설정한다. 추상모델 자신은 테이블을 생성하지 않고, 추상모델을 상속받는 하위 모델들에서 필드들을 생성한다.  


~~~
from django.db import models

class CommonInfo(models.Model):
	name = models.CharField(max_length = 100)
	age = models.PositiveIntegerField()
	
	class Meta: 
		abstract = True
		
class Student(CommonInfo):
	home_group = models.CharField(max_length = 5) 
~~~


`Student` 모델은 `name`, `age`, `home_group`이라는 필드를 가지게 된다.  
상속받은 필드들은 override가능하며 `None`을 사용하여 제거할 수 있다.  

**Meta 상속**  
자식 모델에서 `Meta`를 정의하지 않는다면 부모 모델에서 주어진 `Meta`를 그대로 가져오게 된다.  

~~~
from django.db import models

class CommonInfo(models.Model):
	# .. 
	class Meta: 
		abstract = True
		ordering = ['name']

class Student(CommonInfo):
	# .. 
	class Meta(CommonInfo.Meta):
		db_table = 'student_info' 
		
~~~  

**`related_name`과 `related_query_name`에 주의하기**  

`ForeignKey`와 `ManyToManyField`에 `related_name`과 `related_query_name`을 사용한다면 역행(reverse)이름을 항상 고유값으로 지정해줘야한다. 추상모델을 사용할 경우에는 고유값이 설정되지 않는다면 문제가 발생하는데, 추상모델(부모)의 필드들이 자녀의 필드에 포함되면서 `related_name`과 `related_query_name`이 함께 적용되기 때문이다.  

이런 문제를 해결하기 위해서 `%(app_label)s`와 `%(class)s`를 부모 모델에 사용한다.  
- `%(class)s`는 자식 클래스의 소문자명으로 동적할당 된다.  
- `%(app_label)s`는 자식 클래스가 소속된 앱의 소문자명이 동적으로 할당된다.  

~~~
from django.db import models 

class Base(models.Model):
	m2m = models.ManyToManyField(
		OtherModel,
		related_name = '%(app_label)s_%(class)s',
		reltated_query_name = '%(app_label)s_%(class)s',
	)
	
	
	class Meta:
		abstract = True

class ChildA(Base):
	pass

class ChildB(Base):
	pass 
	
~~~
	

#### 멀티테이블   
모델별로 테이블을 가지면서 상속을 할 수 있는 방식이 멀티테이블 상속방식이다.  

~~~
from django.db import models

class Place(models.Model):
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=80)

class Restaurant(Place):
	serves_hot_dogs = models.BooleanField(default=False)
	serves_pizza = models.BooleanField(default=False) 
	
~~~

`place`와 `Restaurant`는 각각의 테이블을 가지기 때문에 아래와 같은 검색이 가능하다.  

~~~
>>> Place.objects.filter(name="Bob's Cafe")
>>> Restaurant.objects.filter(name="Bob's Cafe")
~~~

만약에 `Place`이면서 `Restaurant`이면 `Place` 객체에서 소문자 이름으로 `Restaurant`객체에 접근이 가능하다.  

~~~
>>> p = Place.objects.get(id=12)  
# 만약에 p가 레스토랑 객체이면 클래스를 반환한다. 
>>> p.restaurant 
<Restaurant: ... > 
~~~

그러나 p가 `Restaurant` 객체가 아니라면(`Place` 객체라던가) 위와 같은 실행문은 `Restaurant.DoesNotExist`를 반환한다.  

`Restaurant`에 자동으로 생성되어 `Place`와 연결시켜주는 `OneToOneField`는 아래와 같다.  

~~~  
place_ptr = models.OneToOneField(
	Place, 
	on_delete=models.CASCADE,
	parent_link = True, 
)
~~~

자동으로 생성되는 필드 대신에 `parent_link=True`를 명시하여 `OneToOneField`를 재정의 할 수 있다.  

**멀티테이블에서 Meta상속**  
멀티테이블 상속의 경우, 별도로 존재하는 테이블이 부모로부터 Meta를 상속받는 것은 말이 되지 않는다. 이미 부모 모델에 존재하는 Meta가 자식 테이블에서 같은 행동을 한다면 모순된 행도응ㄹ 가져오기 일상이다.   

따라서 자식 모델은 부모의 Meta클래스에 접근할 수 없다. 예외적으로 허용되는 상황이 정렬의 경우인데, 이 것은 부모로부터 상속받는다.  


### 프록시 모델  
모델의 파이썬 수준에서의 행동만 변경하고 싶을 경우 프록시 모델을 쓴다.   
`proxy = True`라는 Meta를 선언하면 별도로 테이블을 생성하지 않아도 된다.  

~~~ 
from django.db import models

class Person(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)

class MyPerson(Person):
	class Meta: 
		proxy = True
		
	def do_something(self):
		# .. 
		pass 

~~~ 


`MyPerson` 클래스는 `Person`과 동일하게 테이블을 운영한다. `Person`으로 생성된 인스턴스는 `MyPerson`에도 접근하며, 역방향도 가능하다.  

~~~
>>> p = Person.objects.create(first_name='foobar')
>>> Myperson.objects.get(first_name='foobar')
<MyPerson: foobar>
~~~ 

proxy 모델을 사용하여 모델의 정렬을 다르게 할 수 있다.  

~~~
class OrderedPerson(Person):
	class Meta: 
		ordering = ['last_name']
		proxy = True

~~~
위와같이 프록시를 생성하면 'last_name'필드를 기준으로 정렬이 된 테이블을 불러올 수 있다.  

#### 프록시 모델 매니저  
모델 매니저를 명시하지 않을 경우 부모 모델에서 매니저를 받아온다. 만약에 프록시 모델에서 매니저를 정의할 경우 기본 매니저로 지정된다. (물론 부모 모델이 가지고 있는 매니저 또한 사용이 가능하다)  
위 예시를 활용하여 프록시의 기본 매니저를 만들어본다.  

~~~
from django.db import models 

class NewManager(models.Manager):
	# .. 
	pass
	
class MyPerson(Person):
	objects = NewManager() 	#새로 만든 매니저 할당 
	
	class Meta:
		proxy = True 
		
~~~ 

베이스 클래스(부모 모델)에 새로운 매니저를 만들어서 자식 클래스가 할당하도록 할 수 있다.  

~~~
class ExtraManagers(models.Model):
	secondary = NewManager()
	
	class Meta:
		abstract = True 
	
class Myperson(Person, ExtraManagers):
	class Meta:
		proxy = True 
		
~~~ 

아마도 위와 같이 사용할 경우는 드물겠으나, 가능하다는 것을 기억하자  
