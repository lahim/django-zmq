import zmq
from typing import Any

from djangozmq import settings, models


class SocketManager:
    _ctx = None
    _socket = None

    def __new__(cls) -> Any:
        c = super().__new__(cls)

        if c._ctx is None:
            c._ctx = zmq.Context()
            c._socket = c._ctx.socket(zmq.PUSH)
            c._socket.connect(settings.PULL_SOCKET)
        return c

    def call_task(self, task_name: str, task_kwargs: dict):
        if task_name not in settings.TASKS:
            raise self.TaskDoesNotExist(f'Task: {task_name} does not exist')

        task = models.Task(name=task_name, status=models.TaskStatus.NEW.value)
        task.set_kwargs(task_kwargs)
        task.save()

        self._socket.send_pyobj(task)

    class TaskDoesNotExist(Exception):
        pass
