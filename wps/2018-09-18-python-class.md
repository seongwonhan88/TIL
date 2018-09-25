---
layout: post
title:  "Pyhton Class 이해하기"
author: "Seongwon Han"
---
# Class


```python
class Shop:
    description = 'this is a shop class'
    count = 0 
    shop_list = []
    def __init__(self,name):  #magic method 생성자 method
        self.name = name
        Shop.count += 1
        Shop.shop_list.append(self)
        #self.__class__.shop_list.append(self)
    def __repr__(self):
        return f'{self.name}'
    # class method
    # 첫 번째 매개변수로 항상 클래스 정의 자체가 전달(cls)
    # 클래스 정의가 전달되는 첫 번째 매개변수의 이름은 관용적으로 cls 사용
    @classmethod
    def class_method_example(cls):
        print('class method')
    
    # example -> Shop 으로 만들어진 instance의 개수 확인
    @classmethod
    def get_shop_count(cls):
        return cls.count
        
    @classmethod
    def get_shop_list(cls):
        return cls.shop_list
    
        
```


```python
subway = Shop('Subway')
starbucks = Shop('Starbucks')
```


```python
### instance들은 각각의 스코프를 가지게 되며 직접 접근이 되지 않는다
```


```python
Shop.get_shop_count()
```




    2



## 실습


```python
class Shop:
    def __init__(self, name, shop_type, address):
        self.name = name
        self.shop_type = shop_type
        self.address = address
    def show_info(self):
        print(f'Shop: {self.name} \n type : {self.shop_type} \n address: {self.address}')

    def change_type(self, new_shop_type):
        self.shop_type = new_shop_type
        
```


```python
shop = Shop('Lotteria', 'fast food', 'Seoul')
shop.show_info()
```

    Shop: Lotteria 
     type : fast food 
     address: Seoul



```python
shop.change_type('slowfood')
shop.show_info()
```

    Shop: Lotteria 
     type : slowfood 
     address: Seoul


## 캡슐화

## 속성 접근 지정자의 종류
- private : 정의된 클래스 내부에서만 사용 가능 
- protected : 정의돈 클래스 및 상속받은 클래스 내부에서만 변경 및 사용 가능 
- public : 클래스 외부에서도 변경 및 사용 가능


```python
class Shop:
    def __init__(self, name, shop_type, address):
        self.name = name
        self.__shop_type = shop_type
        self.address = address
    def show_info(self):
        print(f'Shop: {self.name} \n type : {self.__shop_type} \n address: {self.address}')

    def change_type(self, new_shop_type):
        self.__shop_type = new_shop_type
        
```


```python
subway=Shop('subway', 'Sandwich', 'Seoul')
```


```python
subway.__shop_type() # access denied 
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    <ipython-input-40-eee09416b0c8> in <module>()
    ----> 1 subway.__shop_type() # access denied
    

    AttributeError: 'Shop' object has no attribute '__shop_type'



```python
subway.show_info()
```

    Shop: subway 
     type : Sandwich 
     address: Seoul



```python
subway.change_type('Fast Food')
```


```python
subway.show_info()
```

    Shop: subway 
     type : Fast Food 
     address: Seoul



```python
subway.__shop_type = 'Sandwich again'
```


```python
subway.show_info()
```

    Shop: subway 
     type : Fast Food 
     address: Seoul



```python
dir(subway)
```




    ['_Shop__shop_type',
     '__class__',
     '__delattr__',
     '__dict__',
     '__dir__',
     '__doc__',
     '__eq__',
     '__format__',
     '__ge__',
     '__getattribute__',
     '__gt__',
     '__hash__',
     '__init__',
     '__init_subclass__',
     '__le__',
     '__lt__',
     '__module__',
     '__ne__',
     '__new__',
     '__reduce__',
     '__reduce_ex__',
     '__repr__',
     '__setattr__',
     '__shop_type',
     '__sizeof__',
     '__str__',
     '__subclasshook__',
     '__weakref__',
     'address',
     'change_type',
     'name',
     'show_info']




```python
subway.__shop_type
```




    'Sandwich again'




```python
subway.show_info()
```

    Shop: subway 
     type : Fast Food 
     address: Seoul


private type으로 지정하면 이름이 _<classname>__<attribute> 로 지정된다. dir(instance)를 통해 확인 가능하다


```python
subway._Shop__shop_type = 'I can change this'
```


```python
subway.show_info()
```

    Shop: subway 
     type : I can change this 
     address: Seoul


## get/set


```python
class Shop:
    SHOP_TYPE_LIST = ['sandwich','fastfood']
    
    def __init__(self, name, shop_type, address):
        self.name = name
        self.__shop_type = shop_type
        self.address = address
    def show_info(self):
        print(f'Shop: {self.name} \n type : {self.shop_type} \n address: {self.address}')

    def change_type(self, new_shop_type):
        self.__shop_type = new_shop_type
    
    #using this we can retrieve _shop_type info
    #특정 private 속성에 대해 getter 함수만 존재 할 경우 해당속성이 읽기전용이 됨
    def get_shop_type(self):
        return self.__shop_type
    
    #setter attr
    def set_shop_type(self, new_shop_type):
        if new_shop_type in self.SHOP_TYPE_LIST:
            self.__shop_type = new_shop_type
        else:
            print('not the right type choose from {}'.format(', '.join(self.SHOP_TYPE_LIST)))
```


```python
subway = Shop('subway','sandwich','seoul')
subway.get_shop_type()
```




    'sandwich'




```python
subway.set_shop_type('fastfood')
subway.get_shop_type()
```




    'fastfood'




```python
subway.set_shop_type('shop')
```

    not the right type choose from sandwich, fastfood



```python
property
```




    property




```python
class Shop:
    SHOP_TYPE_LIST = ['sandwich','fastfood']
    
    def __init__(self, name, shop_type, address):
        self.name = name
        self.__shop_type = shop_type
        self.address = address
    def show_info(self):
        print(f'Shop: {self.name} \n type : {self.shop_type} \n address: {self.address}')

    def change_type(self, new_shop_type):
        self.__shop_type = new_shop_type
    
    def get_shop_type(self):
        return self.__shop_type
    
    #setter attr
    def set_shop_type(self, new_shop_type):
        if new_shop_type in self.SHOP_TYPE_LIST:
            self.__shop_type = new_shop_type
        else:
            print('not the right type choose from {}'.format(', '.join(self.SHOP_TYPE_LIST)))
    
    #getter
    @property
    def shop_type(self):
        return self.__shop_type
    
    #setter property decorator
    #<getter property method name>.setter
    @shop_type.setter
    def shop_type(self, new_shop_type):
        if new_shop_type in self.SHOP_TYPE_LIST:
            self.__shop_type = new_shop_type
        else:
            print('not the right type choose from {}'.format(', '.join(self.SHOP_TYPE_LIST)))
    
```


```python
subway = Shop('Subway','sandwich','Seoul')
subway.shop_type
```




    'sandwich'




```python
#property makes the return back to the function
subway.shop_type
subway.shop_type = 'fasg'
```

    not the right type choose from sandwich, fastfood


## inheritance

기존 클래스의 모든 요소들을 상속받는 새로운 클래스 


```python

```


```python

```


```python
class Shop:
    SHOP_TYPE_LIST = ['sandwich','fastfood']
    
    def __init__(self, name, shop_type, address):
        self.name = name
        self._shop_type = shop_type
        self.address = address
    def show_info(self):
        print(info)

    def change_type(self, new_shop_type):
        self._shop_type = new_shop_type
    
    def get_shop_type(self):
        return self._shop_type
    
    #setter attr
    def set_shop_type(self, new_shop_type):
        if new_shop_type in self.SHOP_TYPE_LIST:
            self._shop_type = new_shop_type
        else:
            print('not the right type choose from {}'.format(', '.join(self.SHOP_TYPE_LIST)))
 
    @property
    def info(self):
        '''restaurant information is passed'''
        return (f'shop : {self.name} \n'
                f'type : {self.shop_type} \n'
                f'address: {self.address}')
        
    #getter
    @property
    def shop_type(self):
        return self._shop_type
    
    #setter property decorator
    #<getter property method name>.setter
    @shop_type.setter
    def shop_type(self, new_shop_type):
        if new_shop_type in self.SHOP_TYPE_LIST:
            self._shop_type = new_shop_type
        else:
            print('not the right type choose from {}'.format(', '.join(self.SHOP_TYPE_LIST)))
    
```


```python
# Restaurant 클래스의 __init__ 재정의 
# shoptype을 받지 않고 rating을 받음 
# 부모 클래스의 초기화 메서드를 super().__init__()을 사용해 호출하고
# name 에 입력받은 매개변수 name 의 값 
# address에 입력받은 address의 값
# 추가적으로 인스턴스의 rating 속성에 매개변수 rating 값을 할당
```


```python
class Restaurant(Shop):
    def __init__(self, name, address, rating):
        super().__init__(name=name, shop_type='shop', address=address)
        self.rating = rating

    @property
    def info_property(self):
        return 'Restaurant'+super().info_property[4:]
```


```python
sb = Restaurant('starbucks','seoul','10')
sb2 = Shop('starbucks','fastfood','seoul')
```


```python

```
