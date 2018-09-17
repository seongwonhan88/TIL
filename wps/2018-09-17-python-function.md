
# python function(cont)

## closure (함수가 정의된 환경)
함수가 모듈로 활동하게 될 때에 어디까지 영향을 받는가? 
module_a 를 받는 module_b를 만들어보자 

#module_a.py
level = 100
def print_level():
    print(level)

#module_b.py
import module_a
level = 50
def print_level():
    print(level)

module_a.print_level()
print_level()

#python에서 module_b를 실행 할 경우 100 50 이라는 결과값이 출력된다.


하나의 모듈에서 전역 변수로 선언되면 모듈에 영역에 영향을 받게된다.

## 내부함수의 closure


```python
# 함수가 동작하기 위해 필요한 영역을 closure로 받음 
level = 0
def outer():
    level = 50
    def inner():
        nonlocal level
        level += 3 
        print(level)
    return inner 
f1 = outer()
f2 = outer()
```


```python
id(f1)
```




    4346710624




```python
id(f2)
```




    4346708584



## decorator
함수를 받아 다른 함수를 반환하는 함수
1. 기능을 추가할 함수를 인자로 받음 
2. 데코레이터 자체에 추가할 기능을 함수로 정의
3. 인자로받은 함수를 데코레이터 내부에서 적절히 호출
4. 2-3을 행하는 내부함수를 반환

*기존 함수의 동작을 변형시키지 않고!! 가 중요*


```python
def square(x):
    result = x ** 2
    return result

def multi(x,y):
    result = x * y 
    return result
```


```python
result1 = square(3)
result2 = multi(3,5)
```


```python
# def debug 
# 1. 매개변수로 함수 하나를 사용
#    매개변수명은 f 
# 2. 내장함수 wrap을 정의 
#   wrap 함수는 위치인자 묶음과 키워드인자 묶음을 모두 받을 수 있도록 정의
# 3. wrap 함수에서 매개변수 f 실행
#    f 실행 시 위치인자, 키워드인자 전달 > 결과를 result에 할당 
# 4. wrap 함수의 마지막에서 result 값을 리턴 
# 5. debug 함수의 마지막에서 wrap 함수 자체를 리턴

def debug(f):
    def wrap(*args, **kwargs):
        result = f(*args, **kwargs)
        print('args', args)
        print('kwargs', kwargs)
        print('result', result)
        return result
    return wrap

```


```python
# debug 함수의 인자로 square 함수를 자체전달
# 결과값을 decorated_Square 변수에 할당 
# 새 변수를 실행해보기

decorated_square = debug(square)
decorated_square(3)
decorated_multi = debug(multi)
decorated_multi(3,4)
```

    args (3,)
    kwargs {}
    result 9
    args (3, 4)
    kwargs {}
    result 12





    12




```python
decorated_square(3,3)
# original 함수가 받을 수 있는 제약을 동시에 따라간다 
```

## decorator 형식을 가진 함수는 @을 사용하여 조금 더 쉽게 활용이 가능하다




```python
@debug
def square(x):
    result = x ** 2
    return result
@debug
def multi(x,y):
    result = x * y 
    return result
```


```python
square(3)

```

    args (3,)
    kwargs {}
    result 9





    9



## Generator
sequence데이터를 사용할 때 사용되는 함수. 데이터 생성을 위한 루틴만 가지고 있음 eg. range()
실제 메모리를 할당하지 않기 때문에 효율적으로 사용하기 위해 사용한다. 


```python
for i in [1,2,3,4,5,6,7,8,9,10]:
    print(i)

```

    1
    2
    3
    4
    5
    6
    7
    8
    9
    10



```python
for i in range(1,11):
    print(i)
```

    1
    2
    3
    4
    5
    6
    7
    8
    9
    10



```python
def range_gen(num):
    i = 0
    while i < num:
        yield i
        i += 1
# yeild 를 넣으면 본인이 호출되기 전까지 대기한다. 그리고 함수는 generator 로 인식된다. 
result = range_gen(10)
print((result))
```

    <generator object range_gen at 0x10316b258>



```python
for i in result:
    print(i)
```


```python
# generator의 경우 자기가 어디까지 할당되는지 알고 있음. 1회성. 
result.__next__
```




    <method-wrapper '__next__' of generator object at 0x10316b048>




```python
result.__next__()
# next의 마지막이 호출되면 iteration(순회)이 멈추며 에러메시지 전달
next(result)
```


    ---------------------------------------------------------------------------

    StopIteration                             Traceback (most recent call last)

    <ipython-input-94-14e0ad753ed4> in <module>()
    ----> 1 result.__next__()
          2 # next의 마지막이 호출되면 iteration(순회)이 멈추며 에러메시지 전달
          3 next(result)


    StopIteration: 


### 아래 예시들은 같은 내용임 magic method 활용


```python
print(result)
```

    <generator object range_gen at 0x10316b258>



```python
result.__str__()
```




    '<generator object range_gen at 0x10316b258>'




```python
len('ABCS')
```




    4




```python
'ABCS'.__len__()
```




    4



## 실습


```python
# 1. 매개변수로 문자열을 받고 문자열이 red 면 apple, yellow - banana, green - melon else이면 i don't know return
```


```python
def fruit(arg):
    if arg == 'red':
        return 'apple'
    elif arg == 'yellow':
        return 'banana'
    elif arg == 'green':
        return 'melon'
    else:
        return 'I don\'t know'

fruit('')
```




    "I don't know"




```python
get_fruit_dict = {
    'red': 'apple',
    'yellow' : 'banana',
    'green' : 'melon'
}

def fruit_get(color):
    return get_fruit_dict.get(color, "I don't know")
```


```python
# 2. 1번에서 작성한 함수에 docstring을 작성하여 함수에 대한 설명을 달아보고, help(함수명)으로 해당 설명을 출력해본다.
```


```python
def fruit(arg):
    '''
    this is a function which takes color as  parameter and returns fruit in accorance.
    '''
    if arg == 'red':
        return 'apple'
    elif arg == 'yellow':
        return 'banana'
    elif arg == 'green':
        return 'melon'
    else:
        return 'I don\'t know'
```


```python
help(fruit)
```

    Help on function fruit in module __main__:
    
    fruit(arg)
        this is a function which takes color as  parameter and returns fruit in accorance.
    



```python

def take_number(*arg):
    
    if len(arg) == 1:
        result = list(arg)
        return result[0]**2
    
    elif len(arg) == 2:
        num1, num2 = arg
        result = num1 * num2
        return result

take_number(5)
```




    25




```python
def take_one_or_two(arg1, arg2=None):
    if arg2:
        return arg1*arg2
    else: 
        return arg1**2
```


```python
#위치인자 묶음을 매개변수로 가지며, 위치인자가 몇 개 전달되었는지를 print하고 개수를 리턴해주는 함수를 정의하고 사용해본다.
def print_return(*args):
    result = len(args)
    return result

print_return('param1','param2')
```




    2




```python
# 람다함수와 리스트 컴프리헨션을 사용해 한 줄로 구구단의 결과를 갖는 리스트를 생성해본다.
# for x in range(1,9):
#     for y in range(1,9):
#         print(f'{x} x {y} = {x*y}')

# multi = [x*y for x in range(1,10) for y in range(1,10)]

def make_str(x,y):
    return f'{x} * {y} = {x*y}'
multiplication = [(lambda x,y : f'{x}*{y}={x*y}')(a,b) for a in range(2,10) for b in range(2,10)]
```


```python

```
