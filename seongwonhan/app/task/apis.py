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
            return Response(data=(context, serializer.data), status=status.HTTP_201_CREATED)
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
                return Response(data=(context, serializer.data), status=status.HTTP_206_PARTIAL_CONTENT)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        context = {"message": "task doesn't exist"}
        return Response(context, status=status.HTTP_404_NOT_FOUND)

