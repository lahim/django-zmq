import uuid
import enum
import json
import importlib
import time

from django.db import models
from django.utils.translation import gettext_lazy as _


class TaskStatus(enum.IntEnum):
    FAILED = -1
    NEW = 0
    QUEUED = 1
    IN_PROGRESS = 2
    COMPLETED = 3


class BaseModel(models.Model):
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('Modified on'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('Created on'))

    class Meta:
        abstract = True


class Task(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    status = models.IntegerField(default=TaskStatus.NEW.value, verbose_name=_('Status'))
    error = models.CharField(null=True, blank=True, max_length=255, verbose_name=_('Error'))
    execution_time = models.FloatField(null=True, verbose_name=_('Execution time in seconds'))
    kwargs = models.CharField(null=True, blank=True, max_length=255, verbose_name=_('Task kwargs'))

    def set_kwargs(self, kwargs: dict):
        self.kwargs = json.dumps(kwargs)

    def get_kwargs(self):
        return json.loads(self.kwargs)

    def get_module(self):
        return '.'.join(self.name.split('.')[:-1])

    def get_function(self):
        return self.name.split('.')[-1]

    def execute(self):
        if self.status not in [TaskStatus.QUEUED.value]:
            raise self.InvalidStatus(f'Task is not in QUEUED status. Current status: {self.status}')

        start_time = time.time()

        self.status = TaskStatus.IN_PROGRESS.value
        self.save()

        try:
            module = importlib.import_module(self.get_module())
            task_fun = getattr(module, self.get_function())
            task_fun(**self.get_kwargs())
        except Exception as err:
            self.status = TaskStatus.FAILED.value
            self.error = str(err)
        else:
            self.status = TaskStatus.COMPLETED.value

        self.execution_time = time.time() - start_time
        self.save()

    def __str__(self):
        return f'{self.uuid}: {self.name}'

    class InvalidStatus(Exception):
        pass
