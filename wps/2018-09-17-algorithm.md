
# 알고리즘

### 순차검색

1. 문자열과 키 문자 한개를 받는 함수구현 
2. while 문을 이용, 문자열에서 키가 존재하는 index 위치 검사 후 해당 index 리턴
3. 찾지 못할 경우 -1을 리턴


```python
sample = "ABCDEFGHIJKLMN"

def sequencial_search(string, key):
    i = 0 
    while i < len(string):
        if string[i] == key:
            return i
        i += 1
    else:
        return -1
```


```python
result = sequencial_search('ABCDE','F')
print(result)
```

    -1


### index 0 부터 증가시키면서 원하는 타겟이 나올 때 까지 비교한다.

### 선택정렬


```python
sample = [9,1,6,8,4,3,2,0,5,7]
len_list = len(sample)

for x in range(len_list-1):
    print(f'current x loop is: {x}')
    cur_min_index = x
    for index in range(x, len_list):
        if sample[cur_min_index] > sample[index]:
            cur_min_index = index
            
#     print(f'{x} loop {sample}')
#     print(f'{x} th loop\'s index is {cur_min_index}, value is {sample[cur_min_index]}')
    
    sample[cur_min_index],sample[x] = sample[x], sample[cur_min_index]
    print(f'current list {sample}')
    
```

    current x loop is: 0
    current list [0, 1, 6, 8, 4, 3, 2, 9, 5, 7]
    current x loop is: 1
    current list [0, 1, 6, 8, 4, 3, 2, 9, 5, 7]
    current x loop is: 2
    current list [0, 1, 2, 8, 4, 3, 6, 9, 5, 7]
    current x loop is: 3
    current list [0, 1, 2, 3, 4, 8, 6, 9, 5, 7]
    current x loop is: 4
    current list [0, 1, 2, 3, 4, 8, 6, 9, 5, 7]
    current x loop is: 5
    current list [0, 1, 2, 3, 4, 5, 6, 9, 8, 7]
    current x loop is: 6
    current list [0, 1, 2, 3, 4, 5, 6, 9, 8, 7]
    current x loop is: 7
    current list [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    current x loop is: 8
    current list [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]



```python
sample = [9,1,6,8,4,3,2,0,5,7]
len_sample = len(sample)
```


```python
print(len_sample)
```

    10



```python
for x in range(len_sample-1):
    lowest = x #index
    for index in range(x, len_sample):
        if sample[index] < sample[lowest]:
            lowest = index
            print(f'smaller than lowest {sample[index]}')
    sample[x],sample[lowest] = sample[lowest], sample[x]
            
```


```python
print(sample)
```

    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]



```python

```
