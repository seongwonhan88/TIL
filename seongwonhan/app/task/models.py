from django.db import models

class Task(models.Model):
    """
    self-recursive model
    """
    task_title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)
    parent_tasks = models.ForeignKey('self', related_name='child_tasks', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_title

