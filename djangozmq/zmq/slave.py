"""
Slave connects to the master and pull all incoming data with defined tasks. Next, imports the tasks
which needs to perform. On receiving a data, it calls the relevant task function with relevant arguments.
"""

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
            task = socket.recv_pyobj()
            task.execute()
        except Exception as err:
            logger.error(err)

    socket.close()
    context.term()


if __name__ == '__main__':
    run()
