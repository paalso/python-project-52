from django.db import models

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import CustomUser


class Task(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT,
                               related_name='tasks')
    labels = models.ManyToManyField(Label, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                               related_name='authored_tasks')
    executor = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                                 related_name='executed_tasks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
