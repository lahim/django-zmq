import importlib
import logging
import zmq

from djangozmq import settings

logger = logging.getLogger(settings.LOGGER_NAME)

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.connect(settings.PUSH_SOCKET)

logger.debug('-' * 120 + '\n>>> ZMQ TASKS <<<\n' + f'{settings.TASKS}\n' + '-' * 120)


def run():
    while True:
        try:
            task_data = socket.recv_json()
            task = task_data.pop('task')
            task_kwargs = task_data.pop('kwargs')

            logger.debug(f'task from socket: {task}')

            if task in settings.TASKS:
                func_name = task.split('.')[-1]
                module_name = '.'.join(task.split('.')[:-1])
                module = importlib.import_module(module_name)
                task_fun = getattr(module, func_name)
                task_fun(**task_kwargs)

                logger.debug(f'task: {task}, kwargs: {task_kwargs}')
                logger.debug(f'task: {task} done')
        except Exception as err:
            logger.error(err)

    socket.close()
    context.term()


if __name__ == '__main__':
    run()
