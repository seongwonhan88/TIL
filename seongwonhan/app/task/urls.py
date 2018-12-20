from django.urls import path

from task.apis import TaskAPIView

app_name = 'apis'
urlpatterns = [
    path('tasks/', TaskAPIView.as_view())
]