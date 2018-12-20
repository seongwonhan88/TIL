---  
layout: single  
toc : true  
author: "Seongwon Han"  
title: "Django: Self-recursive model API 구현하기"
tags: django python drf
category: how-to 
---  


## DRF로 Self-Recursive Model데이터 

### 설계 요구사항
1) TASK 생성/변경/삭제 가능 
> CRUD 기능 구현

2) TASK 하위에 TASK를 생성 가능, 하위 TASK 깊이 제한 없음     
> 모델 자신을 Foreign Key로 참조   

3) 유저 개념 없음  
4) TASK간 순서 개념 관리 없음 


### Model 구현

모델은 간단하게 자신을 참조하도록 parent_task를 Foreign Key로 잡도록 했다. 

~~~ 
class Task(models.Model):
    """
    self-recursive model
    """
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    parent_tasks = models.ForeignKey('self', related_name='child_tasks', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

~~~


### API, Serializer 구현

Django 모델은 self-recursive가 가능하지만, DRF 내부적인 Serializer의 경우는 serializer자신을 바로 참조 할 수 없다. 
이를 위해서 `djangorestframework-recursive`를 활용했다. 

먼저 pip를 통해 `djangorestframework-recursive`를 설치한다. 자세한 내용은 [drf-recursive github](https://github.com/heywbj/django-rest-framework-recursive/blob/master/tests/test_recursive.py) 페이지 참조

#### installation
~~~
pip install djangorestframework-recursive
~~~

#### 적용
~~~
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    child_tasks = RecursiveField(allow_null=True, many=True, required=False)
    class Meta:
        model = Task
        fields = (
            'pk',
            'title',
            'created_at',
            'modified_at',
            'completed',
            'child_tasks',
        )

~~~

api로 제공을 할 때 가독성을 높이기 위한 방법을 찾느라 좀 시간이 걸렸다. 

희망하던 API의 형태는 아래와 같다. 

~~~
{
	"pk": 1,
	"title": "parent_task",
	"child_tasks": [
		{
			"pk": 2, 
			"title": "child_task",
			"child_tasks": [
				{
					"pk": 3,
					"title": "grand_child_task",
					"child_tasks": [
						{...}
					]
				}
			]
		}
	]
}

~~~

이렇게 표현되기 위해서는 몇가지 선행 작업이 필요하다. 

1) parent_tasks가 존재하지 않는 항목들만 가져와야 한다.   
2) serializer에 보여줄 필드를 related_name을 적어준다.  

#### serializer.py

~~~
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    child_tasks = RecursiveField(allow_null=True, many=True, required=False)
    class Meta:
        model = Task
        fields = (
            'pk',
            'title',
            'created_at',
            'modified_at',
            'completed',
            'child_tasks',
        )

~~~


#### api.py

~~~
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TaskSerializer
from .models import Task


class TaskAPIView(APIView):

    def get(self, request):
        task = Task.objects.filter(parent_tasks__isnull=True)
        if task.exists():
            serializer = TaskSerializer(task, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {"message": "task successfully created"}
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        task = Task.objects.get(id=request.data.get('task_id'))
        if task:
            task.delete()
            context = {"message": "task successfully deleted"}
            return Response(context, status=status.HTTP_204_NO_CONTENT)
        context = {"message": "task doesn't exist"}
        return Response(context, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request):
        task = Task.objects.get(id=request.data.get('task_id'))
        if task:
            serializer = TaskSerializer(task, partial=True, data=request.data)
            if serializer.is_valid():
                serializer.save()
                context = {"message": "task successfully updated"}
                return Response(context, status=status.HTTP_206_PARTIAL_CONTENT)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        context = {"message": "task doesn't exist"}
        return Response(context, status=status.HTTP_404_NOT_FOUND)

~~~

### 결론
스스로를 참조하는 모델을 API로 구현하기 위해서는 reverse로 어떻게 접근을 하는지 명확한 이해가 필요하다.  
따라서 Django를 사용할 경우 `related_name` 사용에 주의하며, 또한 API 쿼리 설정 시 Front 가독성이 편리하도록 구성을 하여 제공하는 것이 필요하다.

### [Github Repository](https://github.com/seongwonhan88/self-recursive-task)