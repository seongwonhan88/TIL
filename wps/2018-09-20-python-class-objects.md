
# Class & Object

## 객체 Object란 무엇인가
한마디로 ***커스텀 자료구조***  
객체는 **Attribute(변수/속성)와 Method(함수)** 두 가지를 포함한다.  

### `class` 선언하기  
클래스는 '구조의 틀'이라고 말할 수 있다. 클래스 선언은 아래와 같이 한다.


```python
class Person():
    pass
```

위에 보여지는 클래스는 빈 클래스 이며, 객체를 생성하기 위한 최소한의 정의다.  
함수처럼 클래스 이름을 호출하여 클래스로부터 객체를 생성할 수 있다.  


```python
someone = Person()
```

위와 같은 방법으로 `someone` 이라는 변수에 클래스를 할당했지만, Person 클래스는 비어있기 때문에 아무 역할도 하지 않는다.  

### 객체 초기화  
아래와 같은 방법으로 클래스를 초기화 해본다.


```python
class Person():
    def __init__(self):
        pass
```

`__init__` 함수를 호출하면서 `self`를 첫 번째 매개변수로 할당한다. `self`는 예약어가 아니지만 이반적으로 이렇게 사용한다.  
위에 초기화 한 객체 또한 아무런 역할을 하지 않는다. 무언가를 하는 객체를 아래와 같이 만들어본다. 


```python
class Person():
    def __init__(self, name):
        self.name = name
```

Person 클래스는 name이라는 매개변수를 초기화 메서드에 추가하는데, 아래 예제를 보면 이해가 조금 더 쉽다.


```python
someone = Person('Homer Simpson')
```


```python
someone.name
```




    'Homer Simpson'



코드의 동작은 아래와 같은 순서로 진행된다.  
 - `Person class`의 정의를 찾는다.
 - 새 객체를 메모리에 초기화(생성)한다.
 - 객체의 `__init__` 메서드를 호출한다. 새롭게 생성된 객체를 `self`에 전달하고 인자(`'Homer Simpson'`)를 `name`에 전달한다. 
 - 객체에 `name`값을 저장한다. 
 - 새로운 객체를 반환한다
 - `someone`에 이 객체를 연결한다

`someone` 의 `name` 값에는 객체의 속성이 저장되어 있으며, 이 속성은 직접 읽고 쓸 수 있다.


```python
print('My name is',someone.name)
```

    My name is Homer Simpson


*Person class에서 name 속성에 접근은 self.name으로 한다. someone이라는 객체를 생성하면 someone.name으로 여긴다.*  
*모든 클래스에서 `__init__`메서드를 가질 필요는 없다.*

## 상속  
기존 클래스에서 일부를 추가하거나 변경하여 새로운 클래스를 생성하는 것을 말한다.  
상속을 이용하면 새로운 클래스는 기존 클래스를 복사하지 않고, 기존 클래스의 모든 것을 쓸 수 있다.  
기존 클래스는 **부모**/슈퍼/베이스 클래스라 불리며, 새 클래스는 **자식**/서브/파생 클래스라 불린다.  
(편의상 부모 클래스, 자식 클래스라 부른다)

위에서 만든 Person 클래스를 활용하여 상속의 개념을 이해해보자


```python
class Person():
    def __init__(self, name):
        self.name = name

class Child(Person): # 상속받는 클래스를 괄호안에 넣어준다.
    pass
```


```python
someone = Person('Homer Simpson')
someone_else = Child('Bart Simpson')
```

`someone_else`는 `Child` 새로운 클래스의 객체이지만 `Person`을 상속받기 때문에 부모 클래스와 같이 `self.name`이라는 초기화 함수를 상속받는다.


```python
someone_else.name
```




    'Bart Simpson'



### 메서드 오버라이드  
자식 클래스가 상속받은 부모 클래스의 메서드를 덮어쓰고 싶을때는 어떻게 할까?  


```python
class Person():
    def __init__(self, name):
        self.name = name

    def introduction(self):
        print(f'Hey! my name is {self.name}! I am a parent!')
        print('DOH!')

class Child(Person): 
    def introduction(self):
        print(f'Hey! my name is {self.name}! I am a child!')
        print('Come on!')
```


```python
someone = Person('Homer Simpson')
someone_else = Child('Bart Simpson')
```

처음 만들때와 크게 다르지 않지만 이번에는 `introduction`이라는 메서드를 생성했다.  
자식 클래스에서 `introduction` 메서드를 오버라이드를 하지 않는다면 `Person`으로부터 받은 메서드가 작동하겠지만  
위와같이 같은 메서드를 입력하면 `Child`클래스 만의 별도 메서드가 출력된다. 


```python
someone.introduction()
```

    Hey! my name is Homer Simpson! I am a parent!
    DOH!



```python
someone_else.introduction()
```

    Hey! my name is Bart Simpson! I am a child!
    Come on!


## 메서드 추가하기  
자식 클래스는 또한 부모 클래스에 없는 메서드를 추가할 수 있다. 

`Child`클래스에만 있는 `hobby()`메서드를 정의해보자 


```python
class Person():
    def __init__(self, name):
        self.name = name

class Child(Person): 
    def hobby(self):
        print('My hobby is skateboarding!')
```


```python
someone = Person('Homer Simpson')
someone_else = Child('Bart Simpson')
```

`someone_else`객체는 `hobby()`객체를 불러 올 수 있다.


```python
someone_else.hobby()
```

    My hobby is skateboarding!


### 부모에게 도움받기: super  
자식 클래스에서 부모 클래스의 메서드를 호출할때 사용한다.  
예제를 보면서 어떻게 부르는지 확인해보자


```python
class Person():
    def __init__(self,name):
        self.name = name

class Child(Person):
    def __init__(self, name, toy):
        super().__init__(name)
        self.toy = toy
```

`Child` 클래스는 `name` 과 `toy`를 매개변수로 받지만 선언을 할 때에 `self.name`으로 하지 않았다.  
위에 상속에서 언급했듯이 같은 내용의 메서드가 자식 클래스에 추가될 경우 오버라이드 됨에 따라 새로 정의를 해줘야 하는데,  
부모 클래스가 받고 있는 `name`매개변수를 추가로 만들지 않기 위해서 `super().__init__`에 있는 것을 그대로 가져온 것을 볼 수 있다.   


코드를 실행하면 아래와 같이 진행된다. 
 - `super()`메서드는 부모 클래스`(Person)`의 정의를 얻는다
 - `__init__()` 메서드는 `Person.__init__()`메서드를 호출한다. 이 메서드는 `self` 인자를 부모 클래스로 전달하는 역할을 한다. 그러므로 부모 클래스에 어떤 선택적 인자를 제공하기만 하면 된다. 이 경우 `Person()`에서 받은 인자는 `name`이다.  
 - `self.toy = toy`는 `Child`클래스를 `Person`클래스와 다르게 만들어주는 새로운 코드다.

이제 `Child`객체를 만들어보자


```python
someone_else = Child('Bart Simpson','skateboard')
```


```python
print(someone_else.name)
print(someone_else.toy)
```

    Bart Simpson
    skateboard


## get/set 속성값과 property  
Python 에서는 다른 언어와 다르게 getter 와 setter가 없지만 property를 활요하여 속성에 접근을 제어할 수 있다.


```python
class Person():
    def __init__(self, name):
        self.__name = name #self.__name 에 '__'를 추가함으로 외부에서 바로 접근이 불가능하게 하였다.
    
    @property
    def person_name(self):
        print('inside the getter')
        return self.__name
    
    @person_name.setter
    def person_name(self, name):
        print('inside the setter')
        self.__name = name        
```


```python
someone = Person('Homer Simpson')
```

아래와 같이 객체에서 매개변수로 지정한 속성에 바로 접근을 하려하면 에러 메시지를 던진다.


```python
someone.name
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-58-11826d80aa2e> in <module>()
    ----> 1 someone.name
    

    AttributeError: 'Person' object has no attribute 'name'


그렇지만 `getter`와 `setter` 역할로 지정한 property를 호출하여 간접적인 접근이 가능하다.


```python
someone.person_name #보기와 같이 person_name뒤에 ()를 붙이지 않는다.
```

    inside the getter





    'Homer Simpson'




```python
someone.person_name = "Bart Simpson"
someone.person_name
```

    inside the setter
    inside the getter





    'Bart Simpson'



위와 같이 변수 값 선언과 같은 방법으로 속성값을 바꿔 줄 수 있게된다.

## Name mangling  
위 예시에서 봤듯이 '__' 를 속성 앞에 붙이면 외부에서 실수로 접근하게 되는 일은 없게 된다.

## 메서드 타입  
어떤 데이터(속성)와 함수(메서드)는 클래스 자신의 일부고, 어떤것은 클래스로부터 생성된 객체의 일부다.  

1. 클래스 정의에서 메서드 첫 인자가 `self`라면 이 메서드는 인스턴스 메서드(instance method)다.  
    - 인스턴스 메서드의 첫 번째 매개변수는 `self`고, 파이썬은 이 메서드를 호출할 때 객체를 전달한다.  
    
2. 이와 반대로 클래스 메서드(class method)는 **클래스 전체에 영향을 미친다**  
    - 클래스 정의에서 함수에 `@classmethod` 데커레이터가 있다면 클래스 메서드다. 
    - 보통 파이썬에서 cls를 사용한다.


```python
class Person():
    count = 0
    def __init__(self):
        Person.count += 1
#     def exclaim(self):
#         print(f'my name is {self.name} !')
    @classmethod
    def clone(cls):
        print(f'This class has {cls.count} clones!')
```


```python
someone_a = Person()
someone_b = Person()
someone_c = Person()
```


```python
Person.clone()
```

    This class has 3 clones!


 위 예제에서와 같이 Person 클래스는 자신이 생성될 때 인스턴스 메서드에서 count값이 1씩 증가한다.  
 아울러 클래스 메서드 clone(cls)가 선언되어 있어서 클래스 변수인 count의 값을 출력한다.  
 **(별 것 아니게 보이지만 클래스 메서드는 본인을 참조하여 함수화 할 수 있다는 것을 꼭 기억해야한다)**

## 덕 타이핑  
파이선은 클래스에 상관없이 같은 동작을 다른 객체에서 적용할 수 있다.  
이름하여 **다형성 polymorphism**


```python
class Quote():
    def __init__(self, person, words):
        self.person = person
        self.words = words
    def who(self):
        return self.person
    def says(self):
        return self.words + '.'
```

위와 같이 `Quote` 라는 클래스는 인스턴스 메서드의 매개변수로  
- `person`과 `words`를 받고   
- 각각의 인자를 리턴하는 `who`와 `says`메서드를 가지고 있다.  


```python
class QuestionQuote(Quote):
    def says(self):
        return self.words + '.'
class ExclamationQuote(Quote):
    def says(self):
        return self.words + '!'
```

`Quote` 클래스를 부모로 상속받아 `says` 메서드를 오버라이드 하는 클래스 둘을 더 만들었다. 


```python
someone_a = Quote('Homer Simpson','Doh!')
someone_b = Quote('Bart Simpson', 'Come on!')
someone_c = Quote('Marge Simpson', 'Homer!')
```


```python
print(f'{someone_a.who()} says {someone_a.says()}')
print(f'{someone_b.who()} says {someone_b.says()}')
print(f'{someone_c.who()} says {someone_c.says()}')
```

    Homer Simpson says Doh!.
    Bart Simpson says Come on!.
    Marge Simpson says Homer!.


예상했던 결과라면 아래와 같은 클래스를 생성해보자


```python
class BabblingBrook():
    def who(self):
        return 'Brook'
    def says(self):
        return 'Babble'
```


```python
brook = BabblingBrook()
```

`BabblingBrook`클래스는 위에 `Quote`클래스들과 전혀 연관이 없다. 그러나 아래를 보게 되면...


```python
def who_says(obj):
    print(obj.who(), 'says', obj.says())
```


```python
who_says(someone_a)
who_says(someone_b)
who_says(someone_c)
who_says(brook) # 전혀 상관없는 1인
```

    Homer Simpson says Doh!.
    Bart Simpson says Come on!.
    Marge Simpson says Homer!.
    Brook says Babble


상관없지만 클래스가 가지고 있는 메서드가 같다면 작동은 동일하게 한다. 이런 행위를 덕타이핑(duck typing)이라 한다.

## 특수메서드  
`__init__`과 같이 이미 파이썬에서 built-in으로 지정된 메서드들이 존재하는데 이들을 특수메서드라 부른다.

|비교연산 메서드|내용|연산|  
|:---- |:--------:| ----:|  
|`__eq__(self, other)`|equal to|`self==other`|  
|`__ne__(self, other)`|not equal to|`self!=other`|  
|`__lt__(self, other)`|less than|`self<other`|  
|`__gt__(self, other)`|greater than|`self==other`|  
|`__le__(self, other)`|less than or equal to|`self<=other`|  
|`__ge__(self, other)`|greater than or equal to|`self==other`|  

|산술연산 메서드|내용|연산|  
|:---- |:--------:| ----:|  
|`__add__(self, other)`|add|`self+other`|  
|`__sub__(self, other)`|subtract|`self-other`|  
|`__mul__(self, other)`|multiply|`self*other`|
|`__floordiv__(self, other)`|floor division|`self//other`|
|`__truediv__(self, other)`|true division|`self/other`|
|`__mod__(self, other)`|modulus|`self%other`|
|`__pow__(self, other)`|exponentiation|`self**other`|


```python

```
