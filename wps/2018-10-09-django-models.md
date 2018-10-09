---
layout: single  
toc : true  
title:  "Django: Model 이해하기 1"  
author: "Seongwon Han"  
tags: python django  
category: language
---
> 장고 [공식문서](https://docs.djangoproject.com/en/2.1/topics/db/models/)를 참조하였습니다. 문서의 모든 내용을 번역한 것이 아니고 개인 공부를 하면서 필요한 내용들만 적었습니다. 

## 모델이란?  
- 모델은 데이터가 무엇인지 결정짓는 정보  
- 당신이 저장하는 데이터의 필수 영역과 행동들을 저장한다
- 각 모델은 `django.db.models.Model`을 subclass로 묶는 python class  
- 모델이 가지고 있는 속성은 데이터베이스의 필드를 나타낸다
- 장고는 이를 가지고 자동으로 생성된 데이터베이스 API를 제공한다  

### Quick Example 

아래 예시는 `Person` 모델을 정의하며, `first_name` 과 `last_name` 이라는 속성을 가지고 있다. 

~~~
from django.db import models

class Person(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
~~~

`first_name`과 `last_name`은 모델의 필드가 된다. 각 필드는 클래스 속성으로 지정되며, 각 속성은 데이터베이스 열(column)에 매핑된다.  
위의 `Person` 모델은 아래와 같은 데이터베이스를 만든다.  

~~~
CREATE TABLE myapp_person (
	"id" serial NOT NULL PRIMARY KEY, 
	"first_name" varchar(30) NOT NULL,
	"last_name" varchar(30) NOT NULL
	);
~~~

몇가지 기술적인 내용  
-  `myapp_person`은 모델의 이름을 기반으로 자동 생성되며 override 가능하다. [Table names](https://docs.djangoproject.com/en/2.1/ref/models/options/#table-names) 참조
- `id` 필드 또한 자동으로 생성되며 override 가능하다. [Automatic primary key fields](https://docs.djangoproject.com/en/2.1/topics/db/models/#automatic-primary-key-fields) 참조 
- 위에 `CREATE TABLE` SQL은 'PostgreSQL'문법으로 작성되었지만, 장고에서는 settings에 지정된 데이터베이스 백엔드에 맞게 조정된 SQL을 사용한다.  


## 모델 사용하기  
모델을 정의하였으면, 장고에게 앞으로 정의한 모델을 사용할 것이라고 알려주어야 한다.  
1. setting(`settings.py`)의 `INSTALLED_APPS` 칸에 `models.py`에 정의한 모델명을 추가한다.  
2. 모델을 추가했으면, 장고에 적용을 위해 터미널에서 `./manage.py makemigration`을 실행 후 `./manage.py migrate`를 실행한다.  

## 필드  
- 모델에서 가장 중요하며 유일하게 모델에서 요구되는 항목이 필드이다   
- 필드는 class 속성에 의해 정의된다  
- [models API](https://docs.djangoproject.com/en/2.1/ref/models/instances/)에 정의된 이름과 겹치지 않도록 주의한다.  

예시:  

~~~
from django.db import models

class Musician(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	instrument = models.CharField(max_length=100)
	
class Album(models.Model):
	artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	release_date = models.DateField()
	num_stars = models.IntegerField()
~~~

### 필드타입  
각 필드는 모델의 인스턴스(`instance`)로 적합한 `Field class`여야 한다. 장고는 필드 클래스를 통해 아래 내용을 결정한다.  
- 열 종류(column type), 어떤 종류의 데이터를 저장 하는가?(e.g. INTEGER, VARCHAR, TEXT)  
- 양식 필드(form field)를 렌더링 할 때 사용하게 될 기본 HTML 위젯(e.g <input type="text">, <select>)  
- 장고의 admin 및 자동 생성되는 양식(form)에 필요한 최소 유효성 확인 요구사항(Minimal validation requirements)  

### 필드 옵션  
각 필드는 field-specific 인수들을 받는다. 예를 들어, CharField(+subclasses)는 max_length를 요구하여 데이터베이스에 저장할 VARCHAR의 크기를 지정한다.  

#### null  
**`True`**로 지정할 경우 장고는 NULL값을 데이터베이스에 저장한다. 기본값은 **`False`**  

#### blank  
**`True`**로 지정할 경우 장고는 필드값이 없는 것을 허용한다. 기본값은 **`False`**   
> blank 는 null과 다르다는 것에 주의하자. null은 데이터베이스에 대한 내용이고, blank는 검증에 관련된 내용이다.  
> 어떤 필드에 blank=True로 지정되었다면 **데이터 입력단**에서 아무것도 입력하지 않는 것을 허용하겠다는 말이지 데이터베이스에 이것이 저장될 수 있는 여부와는 관련이 없다. 따라서 blank=True로 한다면 해당 필드가 저장될 데이터베이스에 null=True를 해줘야 한다.  

#### choices  
반복 가능한 튜플 2개 이상이 있으면 필드에서 선택사항(choice)로 사용될 수 있다.  

~~~
YEAR_IN_SCHOOL_CHOICES = (
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    ('SR', 'Senior'),
    ('GR', 'Graduate'),
)
~~~

튜플의 첫번째 항목이 데이터베이스에 저장될 것이며, 두번째 항목이 사용자에게 노출된다.  
모델 인스턴스가 주어지면 choices는 `get_FOO_display()` 메소드를 통해 접근할 수 있다.  

~~~
from django.db import models

class Peron(models.Model):
	SHIRT_SIZES = (
		('S', 'Small'),
		('M', 'Medium'),
		('L', 'Large'),		
	)
	name = models.CharField(max_length=60)
	shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)
~~~

~~~
>>> p = Person(name="Fred Flintstone", shirt_size="L")
>>> p.save()
>>> p.shirt_size
'L'
>>> p.get_shirt_size_display()
'Large' 
~~~


#### default  
필드의 디폴트 값. 특정 값(value)이거나 호출할 수 있는 객체(callable object)일 수 있다. 호출 객체일 경우 새로운 객체가 생성될 때마다 호출된다.  

#### primary_key  
**True**일 경우 해당 필드가 `primary_key`로 설정된다.  
모델이 가지고 있는 어느 필드에도 `primary_key = True`를 지정하지 않을 경우 장고는 자동으로 `IntegerField`를 추가하여 `primary_key`를 가지게 한다.  
`primary_key`는 읽기 전용이다. 만약에 `primary_key`의 값을 변경하고 저장하게 된다면 기존 객체 옆에 새로운 객체가 생성된다. 

~~~
from django.db import models 

class Fruit(models.Model):
	name = models.CharField(max_length=100, primary_key=True) 
~~~

~~~
>>> fruit = Fruit.objects.create(name='Apple')
>>> fruit.name = 'Pear'
>>> fruit.save()
>>> Fruit.objects.values_list('name', flat=True)
<QuerySet ['Apple', 'Pear']>
~~~


#### unique  
**True** 일 경우 해당 필드에 들어가는 값은 테이블에서 유일해야 한다.  

### 자동 primary key 필드  
디폴트에 의해 장고는 각 모델이 아래와 같은 필드를 제공한다.  

~~~
id = models.AutoField(primary_key=True)
~~~

이것은 자동증가하는 primary key다.  
커스텀 primary key를 설정하고 싶으면 `primary_key = True`를 필드에 입력하면 된다.  
각 모델은 하나의 필드당 하나의 `primary_key`를 가지도록 한다. 

### 세부필드명(Verbose Field Names)  
`ForeignKey`, `ManyToManyField`, `OneToOneField`를 제외한 나머지 필드 타입들은 옵션으로 첫번째 인자를 세부필드명으로 받는다. 만약 세부 필드명이 주어지지 않는다면 장고는 자동으로 필드의 속성명을 사용하여 세부명을 생성한다. (이 때 underscore가 space로 변환)  

아래는 "person's first name"이라는 세부명을 가진다:  

~~~
first_name = models.CharField("persons's first name", max_length=30)  
~~~

아래는 "first name"이라는 세부명을 가진다:  

~~~
first_name = models.CharField(max_length=30)  
~~~  

`ForeignKey`, `ManyToManyField`, `OneToOneField`는 첫번째 위치 인자가 모델 클래스임에 따라 `verbose_name`항목을 키워드 인자로 받는다.  

~~~
poll = models.ForeignKey(
	Poll,
	on_delete=models.CASCADE,
	verbose_name = "the related poll",
	)
sites = models.ManyToManyField(Site, verbose_name="list of sites")
plate = models.OneToOneField(
	Place, 
	on_delete=models.CASCADE,
	verbose_name = "related place",
	)
~~~

`verbose_name`에 지정된 첫번째 알파벳을 대문자로 할 필요가 없다. 장고에서 자동으로 처리해준다.  


### Relationships 관계  
관계형 데이터베이스의 강점은 테이블들을 관련시키는 것으로 부터 나온다. 장고는 가장 일반적인 유형 세 가지(`ManyToOne`, `ManyToMany`, `OneToOne`)을 정의하는 방법을 제공한다.  

#### Many-to-one 관계  
many-to-one 관계를 정의하기 위해서 `django.db.models.ForeignKey`를 사용한다. 다른 필드 유형과 마찬가지로 모델의 클래스 속성으로 포함하여 사용한다.  

`ForeignKey`는 위치 인자로 참조할 모델을 요구한다.  

~~~
from django.db import models

class Manufacturer(models.Model):
	# .. 
	pass 
	
class Car(models.Model):
	manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)  
	# .. 
	
~~~ 

ForeignKey를 받는 필드명은 해당 모델을 소문자화 하여 할당하는 것을 추천한다. (필수는 아님)  
또한 자기 스스로를 ForeignKey의 모델로 갖는 재귀관계(recursive relationships)를 생성할 수 있다.  

#### Many-to-many 관계  
many-to-many 관계를 정의하기 위해서 `ManyToManyField`를 사용한다. 다른 필드 유형과 마찬가지로 모델의 클래스 속성으로 포함하여 사용한다.  

`ForeignKey`는 위치 인자로 참조할 모델을 요구한다.    

예를 들어 `Pizza`는 여러가지의 `Topping` 객체를 소유한다. 그리고 `Topping`은 여러가지의 `Pizza`에 올려질 수 있음으로 many-to-many의 관계가 성립한다.  

~~~
from django.db import models 

class Topping(models.Model):
	# ..
	pass 
	
class Pizza(models.Model):
	# ..
	toppings = models.ManyToManyField(Topping)  
~~~  

`ForeignKey`와 마찬가지로 재귀관계를 생성할 수 있으며, 아직 정의되지 않은 모델 또한 참조 할 수 있다.  
> `'Model Name'`을 생성하면, 아직 생성되지 않은 모델이라도 생성된 후 참조할 수 있도록 해준다.  

many-to-many 관계 형성을 할 때에 어떤 모델에 ForeignKey를 주는지는 크게 상관이 없으나(`Pizza`가 `Topping`의 키를 가지던, `Topping`이 `Pizza`의 키를 가지던) 둘 중 하나만 가져야 한다.  

#### Many-to-many 관계의 추가 필드  
피자와 토핑의 관계와 같이 단순한 many-to-many의 관계처리를 할 경우에는 `ManyToManyField`로 처리하면 된다. 그러나 두 모델간의 관계를 데이터로 연결시켜줘야할 경우가 발생하기도 한다.  

예를 들어 음악가들이 소속된 음악 그룹들을 트랙킹하는 애플리케이션의 경우를 살펴보자. many-to-many 관계가 멤버(person)와 그룹(group) 으로 성립이되고 `ManyToManyField`를 사용 할 수 있다. 그러나 멤버쉽에 대하여 더 많은 정보를 얻고 싶을 수 도 있다. (예를들어 언제 그룹에 가입했는지 등)  

이런 상황에서 장고는 many-to-many관계를 정의하는데 사용하게된 모델을 허용한다. 특정 필드를 중간(intermediate)모델로 사용할 수 있다. 중간 모델은 중재 역할을 하는 `through`인자를 사용하여`ManyToManyField`와 연관 짓는다.  

~~~
from django.db import models 

class Person(models.Model):
	name = models.CharField(max_length=128)
	
	def __str__(self):
		return self.name
		
		
class Group(models.Model):
	name = models.CharField(max_length=128)
	members = models.ManyToManyField(Person, through='Membership')
	
	def __str(self):
		return self.name
		

class Membership(models.Model):
	person = models.ForeignKey(Person, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	date_joined = models.DateField()
	invite_reason = models.CharField(max_length=64) 

~~~

중재 역할을 하는 모델을 설정할 경우 many-to-many 관계에 포함되는 foreign key들을 명시적으로 지정해줘야한다.  
	
아울러 중재 모델에는 제약사항들이 있다.  
- 중재 모델은 반드시 한개의 소스 모델의 foreign key를 포함하거나(위 예시의 경우 **Group**이 된다) `ManyToManyField.through_fields`를 사용하여 장고가 사용할 foreign key 를 명시해줘야한다. 만약 한개 이상의 foreign key가 사용되었는데  through_fields에 명시되지 않았다면 에러가 발생한다.  
- 모델이 자신이 스스로를 중재 모델을 통해 many-to-many 관계를 가질 경우(recursive) 두 개의 foreign key를 가지는 것이 허용된다 그러나 이 foreign key들은 각각 다른 모델에서의 many-to-many 관계로 취급될 것이다. (마찬가지로 through_fields를 통해 명시해줘야 한다)   
- 모델에서 스스로 many-to-many 관계를 정의하려 할 때에는 `symmetrical=False`를 사용해야한다.   

~~~
>>> ringo = Person.objects.create(name="Ringo Starr")
>>> paul = Person.objects.create(name="Paul McCartney")
>>> beatles = Group.objects.create(name="The Beatles")
>>> m1 = Membership(person=ringo, group=beatles,
...     date_joined=date(1962, 8, 16),
...     invite_reason="Needed a new drummer.")
>>> m1.save()
>>> beatles.members.all()
<QuerySet [<Person: Ringo Starr>]>
>>> ringo.group_set.all()
<QuerySet [<Group: The Beatles>]>
>>> m2 = Membership.objects.create(person=paul, group=beatles,
...     date_joined=date(1960, 8, 1),
...     invite_reason="Wanted to form a band.")
>>> beatles.members.all()
<QuerySet [<Person: Ringo Starr>, <Person: Paul McCartney>]>
~~~

일반적인 many-to-many 필드와 다르게 `add()`, `create()`, `set()` 메소드로 관계를 생성할 수 없다. 

~~~
>>> #아래 명령어를 입력하면 에러가 발생한다
>>> beatles.members.add(john)
>>> beatles.members.create(name="George Harrison")
>>> beatles.members.set([john, paul, ringo, george])
~~~

안되는 이유를 설명하자면 다음과 같다. Membership 모델에는 Person 과 Group이 공유하지 않는 별도의 필드들이 존재한다. 그렇기 때문에 Person 과 Group만 단순히 연결하고자 하면 추가 필드 값들을 줄 수 없기 때문에 실패하는 것이다. 중재 모델의 인스턴스를 생성하는 방법 외에는 두 모델을 연결 할 방법이 없게된다.  

`remove()` 메소드 또한 같은 이유에서 사용이 불가능하다. 예를들어 중재 모델에 의해 정의된 custom through 테이블이(model1 과 model2)에 고유성을 적용하지 않으면 `remove()`호출은 어떤 중간 모델 인스턴스를 삭제해야하는지에 대한 충분한 정보가 없다. 

~~~
>>> Membership.objects.create(person=ringo, group=beatles,
...     date_joined=date(1968, 9, 4),
...     invite_reason="You've been gone for a month and we miss you.")
>>> beatles.members.all()
<QuerySet [<Person: Ringo Starr>, <Person: Paul McCartney>, <Person: Ringo Starr>]>
>>> # 아래 내용이 성립하지 않는 이유는 어떤 ringo를 제거해야 할 지 모르기 때문이다.  
>>> beatles.members.remove(ringo)
~~~

그러나 `clear()`메소드는 인스턴스의 모든 many-to-many 관계를 삭제 가능하다. 

~~~
>>> # Beatles 가 해체 되었으므로 제거한다. 
>>> beatles.members.clear()
>>> # beatles 인스턴스와 함께 생성된 중개 모델 또한 제거됨을 참고하자. 
>>> Membership.objects.all()
<QuerySet []>
~~~

중재 모델을 통해서 many-to-many 관계를 생성하였으면, 쿼리를 보낼 수 있다. 평범한 many-to-many 관계와 같이 속성을 이용하여 쿼리를 보낸다.  

~~~
# Group의 member의 name 이 'Paul'로 시작하는 모든 결과를 가져온다. 
>>> Group.objects.filter(members__name__startswith='Paul')
<QuerySet [<Group: The Beatles>]>
~~~

중재 모델을 사용함으로써 모델에 해당하는 속성들을 요청할 수 있다.  

~~~
# 'The Beatles' 그룹에서 (Membership Model)의 date_joined가 1961년 1월1일 이후인 멤버를 찾아라. 
>>> Person.objects.filter(
...     group__name='The Beatles',
...     membership__date_joined__gt=date(1961,1,1))
<QuerySet [<Person: Ringo Starr]>
~~~

필요하다면 `Membership`에 직접 정보를 요청할 수 있다.  

~~~
>>> ringos_membership = Membership.objects.get(group=beatles, person=ringo)
>>> ringos_membership.date_joined
datetime.date(1962, 8, 16)
>>> ringos_membership.invite_reason
'Needed a new drummer.'
~~~

위와 같은 정보에 접근하는 다른 방법은 `Person` 객체 통한 many-to-many reverse relationship이다.

~~~
>>> ringos_membership = ringo.membership_set.get(group=beatles)
>>> ringos_membership.date_joined
datetime.date(1962, 8, 16)
>>> ringos_membership.invite_reason
'Needed a new drummer.'
~~~