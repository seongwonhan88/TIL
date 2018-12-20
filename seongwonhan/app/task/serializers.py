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
            'parent_tasks',
        )
