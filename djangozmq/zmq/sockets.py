import zmq
from typing import Any

from djangozmq import settings


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

    def call_task(self, task: str, task_kwargs: dict):
        self._socket.send_json({
            'task': task,
            'kwargs': task_kwargs,
        })
