import enum
import logging
import time
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from . import mixins

logger = logging.getLogger(__name__)


class TaskStatus(enum.IntEnum):
    FAILED = -1
    NEW = 0
    QUEUED = 10
    SCHEDULED = 11
    IN_PROGRESS = 20
    COMPLETED = 30


class BaseModel(models.Model):
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('Modified on'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('Created on'))

    class Meta:
        abstract = True


class Task(mixins.TaskMixin, BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    status = models.IntegerField(default=TaskStatus.NEW.value, verbose_name=_('Status'))
    error = models.CharField(null=True, blank=True, max_length=255, verbose_name=_('Error'))
    execution_time = models.FloatField(null=True, verbose_name=_('Execution time in seconds'))
    kwargs = models.CharField(null=True, blank=True, max_length=255, verbose_name=_('Task kwargs'))

    def on_error(self, err):
        logger.warning(f'Task: {self.name} was not finished - something went wrong. Details: {str(err)}')
        self.status = TaskStatus.FAILED.value
        self.error = str(err)

    def on_success(self, result):
        logger.info(f'Task: {self.name} was finished with success.')
        self.status = TaskStatus.COMPLETED.value

    def post_call(self):
        pass

    def execute(self):
        if self.status not in [TaskStatus.QUEUED.value]:
            raise self.InvalidStatus(f'Task is not in QUEUED status. Current status: {self.status}')

        start_time = time.time()

        self.status = TaskStatus.IN_PROGRESS.value
        self.save()

        self.call()

        self.execution_time = time.time() - start_time
        self.save()

    def __str__(self):
        return f'{self.uuid}: {self.name}'

    class InvalidStatus(Exception):
        pass
