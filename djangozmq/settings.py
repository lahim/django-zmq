from django.conf import settings as django_settings

LOGGER_NAME = 'django-zmq'

DEFAULT_PULL_SOCKET = 'tcp://127.0.0.1:5000'
DEFAULT_PUSH_SOCKET = 'tcp://127.0.0.1:5001'

PULL_SOCKET = getattr(django_settings, 'ZMQ_PULL_SOCKET', DEFAULT_PULL_SOCKET)
PUSH_SOCKET = getattr(django_settings, 'ZMQ_PUSH_SOCKET', DEFAULT_PUSH_SOCKET)

TASKS = getattr(django_settings, 'ZMQ_TASKS', [])
