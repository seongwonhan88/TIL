# SELF-RECURSIVE-TASK

## installation
`pip install -r requirements.txt`


## API 명세서 

### TASK 목록 가져오기 
#### 요청 URI
~~~
GET /api/tasks/
~~~

#### 응답(예시)
~~~
[
    {
        "pk": 1,
        "title": "Build a website",
        "created_at": "2018-12-20T05:08:55.325758Z",
        "modified_at": "2018-12-20T05:08:55.325808Z",
        "completed": false,
        "child_tasks": [
            {
                "pk": 2,
                "title": "get a domain",
                "created_at": "2018-12-20T05:09:12.554377Z",
                "modified_at": "2018-12-20T05:09:12.554567Z",
                "completed": false,
                "child_tasks": []
            },
            {
                "pk": 3,
                "title": "hello world! is added!",
                "created_at": "2018-12-20T07:39:47.621683Z",
                "modified_at": "2018-12-20T05:11:10.122461Z",
                "completed": false,
                "child_tasks": [
                    {
                        "pk": 10,
                        "title": "deploy on aws",
                        "created_at": "2018-12-20T06:25:28.708564Z",
                        "modified_at": "2018-12-20T06:25:28.708637Z",
                        "completed": false,
                        "child_tasks": []
                    }
                ]
            }
        ]
    }
]
~~~

### TASK 생성하기 
#### 요청 URI
~~~
POST /api/tasks/
~~~
 
#### 요청
~~~
{
	"title":"something to do",
	"parent_tasks":1
}
~~~
> "parent_task"는 있을 시 제공, 없을 시 제공하지 않아도 됨

#### 응답
~~~
[
    {
        "message": "task successfully created"
    },
    {
        "pk": 20,
        "title": "something to do",
        "created_at": "2018-12-20T08:05:21.363677Z",
        "modified_at": "2018-12-20T08:05:21.363785Z",
        "completed": false,
        "child_tasks": []
    }
]
~~~

### TASK 업데이트 하기 
#### 요청 URI
~~~
PATCH /api/tasks/
~~~
 
#### 요청
~~~
{
	"task_id": 11,
	"title":"something to do, changing parent!",
	"parent_tasks": 3
}
~~~

#### 응답
~~~
[
    {
        "message": "task successfully updated"
    },
    {
        "pk": 11,
        "title": "something to do, changing parent!",
        "created_at": "2018-12-20T08:10:59.750853Z",
        "modified_at": "2018-12-20T07:39:18.666680Z",
        "completed": false,
        "child_tasks": [],
        "parent_tasks": 3
    }
]
~~~


### TASK 제거 하기 
#### 요청 URI
~~~
DELETE /api/tasks/
~~~
 
#### 요청
~~~
{
	"task_id": 11
}
~~~

#### 응답
~~~
{
    "message": "task successfully deleted"
}
~~~
