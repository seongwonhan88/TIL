---
layout: single  
toc : true  
title:  "Django: Model 이해하기 2"  
author: "Seongwon Han"  
tags: python django  
category: language
---

### One-to-one 관계  
one-to-one 관계를 정의하기 위해서 `OneToOneField`를 사용한다.   
`Place`가 옵션으로 `Restaurant`가 될 수 있는 예를 살펴보자   

`./manage.py startapp one_to_one을 만든 후 models.py에 모델을 정의해본다.  

~~~
from django.db import models

class Place(models.Model):
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=50)
	
	def __str__(self):
		return f'{self.name} the place'

class Restaurant(models.Model):
	place = models.OneToOneField(
		Place,
		on_delete=models.CASCADE,'
		primary_key=True,
		)

	serves_hot_dogs = models.BooleanField(default=False)
	serves_pizza = models.BooleanField(default=False)
	
	def __str__(self):
		return f'{self.place.name} the restaurant'
		
class Waiter(models.Model):
	restaurant = models.ForeignKey(
		Restaurant,
		on_delete = models.CASCADE
		)
		
	def __str__(self):
		return f'{self.name} the water at {self.restaurant}'
~~~

`./manage.py makemigration` > `migrate` 하여 적용한 후 ipython을 실행 하여 아래와 같이 입력해보자 


먼저 `Place` 객체를 만들어보자  

~~~
>>> p1 = Place(name='Demon Dogs', address='944 W. Fullerton')
>>> p1.save()
>>> p2 = Place(name='Ace Hardware', address='1013 N. Ashland')
>>> p2.save()
~~~

그리고 `Restaurant`객체를 만들면서 부모 객체의 ID 값을 이 객체의 ID로 주자.  

~~~
>>> r = Restaurant(place=p1, serves_hot_dogs=True, serves_pizza=False)
>>> r.save()
~~~   

`Restaurant`객체는 place로 접근이 가능하다.  

~~~
r.place
<Place: Demon Dogs the place>  
~~~


`Place`객체 또한 **restaurant이 생성되었다면** 접근이 가능하다  

~~~
>>>p1.restaurant
<Restaurant: Demon Dogs the restaurant>
~~~

`p2`는 아직 연관된 `restaurant`가 존재하지 않는다.  


~~~
>>> from django.core.exceptions import ObjectDoesNotExist
>>> try:
>>> 	p2.restaurant
>>> except ObjectDoesNotExist:
>>> 	print("There is no restaurant here.")
There is no restaurant here. 

~~~

우리는 이미 `p2`에 연결된 Restaurant객체가 없는 것을 알지만, 매번 이런식으로 검사할 수 없기 때문에, `hasattr`이라는 함수를 사용하여 사전에 확인이 가능하다.    


~~~
>>> hasattr(p2, 'restaurant')
False
~~~  

`p2`를 `r.place`에 할당해본다 하자.  

~~~
>>> r.place = p2
>>> r.save()
>>> p2.restaurant
<Restaurant: Ace Hardware the restaurant>
>>> r.place
<Place: Ace Hardware the place>
~~~

`place`가 `Restaurant`의 primary key이기 때문에 `save()`를 하게 되면 새로운 restaurant 객체를 생성하게 된다.   
> 이제 r의 값이 P2로 변경되었다.  

다시 place 를 원래대로 복구하려면 역방향으로 지정을 해도 된다.  

~~~
>>> p1.restaurant = r 
>>> p1.restaurant
<Restaurant: Demon Dogs the restaurant> 
~~~  

객체는 반드시 one-to-one 관계를 가지기 전에 저장을 해야한다. 예를들어 `Restaurant`객체를 저장하지 않은 `Place` 객체로 생성하려 하면 `ValueError`를 발생시킨다.  

~~~
>>> p3 = Place(name='Demon Dogs', address='944 W. Fullerton')
>>> Restaurant.objects.create(
>>> 	place=p3, 
>>> 	serves_hot_dogs=True,
>>> 	serves_pizza=False,
>>> 	)
Traceback (most recent call last):
...
ValueError: save() prohibited to prevent data loss due to unsaved related object 'place'.
~~~

`Restaurant.objects.all()`을 호출하면 `Restaurant` 객체의 쿼리셋들을 반환한다. `r.place = p2` 로 할당한 `Ace Hardware the restaurant`도 있는 것을 발견 할 수 있다.  

~~~
>>> Restaurant.objects.all()  
<QuerySet [<Restaurant: Demon Dogs the restaurant>, <Restaurant: Ace Hardware the restaurant>]>  
~~~

`Place.objects.all()`을 호출하면 `Restaurant` 객체가 있건 없건 상관없이 `Place`객체의 쿼리셋을 반환한다.  

~~~
>>> Place.objects.order_by('name')
<QuerySet [<Place: Ace Hardware the place>, <Place: Demon Dogs the place>]>
~~~  

관계들을 통하여 쿼리를 요청할 수 있다.  

~~~
>>> Restaurant.objects.get(place=p1)
<Restaurant: Demon Dogs the restaurant>
>>> Restaurant.objects.get(place__pk=1)
<Restaurant: Demon Dogs the restaurant>
>>> Restaurant.objects.filter(place__name__startswith="Demon")
<QuerySet [<Restaurant: Demon Dogs the restaurant>]>
>>> Restaurant.objects.exclude(place__address__contains="Ashland")
<QuerySet [<Restaurant: Demon Dogs the restaurant>]>  
~~~

이는 역방향으로도 통한다.  

~~~
>>> Place.objects.get(pk=1)
<Place: Demon Dogs the place>
>>> Place.objects.get(restaurant__place=p1)
<Place: Demon Dogs the place>
>>> Place.objects.get(restaurant=r)
<Place: Demon Dogs the place>
>>> Place.objects.get(restaurant__place__name__startswith="Demon")
<Place: Demon Dogs the place>
~~~

`Restaurant`객체에 `Waiter`객체를 하나 생성해보자   

~~~
>>> w = r.waiter_set.create(name='Joe')
>>> w
<Waiter: Joe the waiter at Demon Dogs the restaurant>
~~~

그리고 `Waiter`의 객체들을 불러오는 방법은 아래와 같다.   

~~~
>>> Waiter.objects.filter(restaurant__place=p1)
<QuerySet [<Waiter: Joe the waiter at Demon Dogs the restaurant>]>
>>> Waiter.objects.filter(restaurant__place__name__startswith="Demon")
<QuerySet [<Waiter: Joe the waiter at Demon Dogs the restaurant>]>
~~~
