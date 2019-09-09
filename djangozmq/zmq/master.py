import zmq
import logging

from djangozmq import settings

logger = logging.getLogger(settings.LOGGER_NAME)


def run():
    context = zmq.Context()
    pull_socket = context.socket(zmq.PULL)
    pull_socket.bind(settings.PULL_SOCKET)

    push_socket = context.socket(zmq.PUSH)
    push_socket.bind(settings.PUSH_SOCKET)

    while True:
        try:
            task_data = pull_socket.recv_json()
            push_socket.send_json(task_data)
        except Exception as err:
            logger.error(err)

    pull_socket.close()
    push_socket.close()
    context.term()


if __name__ == '__main__':
    run()
