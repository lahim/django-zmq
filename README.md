# Django-ZMQ
Simple integration ZMQ with Django.

[![Build Status](https://travis-ci.org/lahim/django-zmq.svg?branch=master)](https://travis-ci.org/lahim/django-zmq)


## Quick start

1. Add "django-zmq" to your INSTALLED_APPS setting like this:
```text
INSTALLED_APPS = [
...
'djangozmq',
]
```

2. Add ZMQ settings into the `settings.py` file, example below:
```python
ZMQ_PULL_SOCKET = 'tcp://127.0.0.1:5000'
ZMQ_PUSH_SOCKET = 'tcp://127.0.0.1:5001'
ZMQ_TASKS = [
    'exampleapp.tasks.send_text_message',
]
```

3. Run ZMQ master using below django command:
```bash
./manage.py zmqrunmaster
```

4. Run ZMQ slave using below django command:
```bash
./manage.py zmqrunslave
```

5. Now, you can send data to the socket as presented below:
```python
import zmq 
 
ctx = zmq.Context() 
task_socket = ctx.socket(zmq.PUSH) 
task_socket.connect('tcp://127.0.0.1:5000')                                                                                                                                                                

task_socket.send_json({ 
        'task': 'exampleapp.tasks.send_text_message', 
        'kwargs': {'a': 1, 'b': 2, 'c': 3, 'd': 4}, 
    }) 
```

## Example:

Below you can find a tasks definition:
`exampleapp/tasks.py`:
```python
def send_text_message(*args, **kwargs):
    print('Sending text message...')
    # add your code here for sending text message...
    print('Text message was sent.')
```

Here is an example of calling a task from your django app:
```python
from djangozmq.zmq.sockets import SocketManager                                                                                                                                                            

sm = SocketManager()                                                                                                                                                                                       
sm.call_task('exampleapp.tasks.send_text_message', {'foo': 'bar'})                                                                                                                                     
```

## Periodic tasks

1. For periodic tasks you need to run django-zmq beat using below command:
```bash
./manage.py zmqrunbeat
```

2. Add periodic tasks into the `settings.py` - example below:
```python
...
ZMQ_PERIODIC_TASKS = [
    ('exampleapp.tasks.check_all_not_completed_jobs', None, 10),
]
```

`ZMQ_PERIODIC_TASKS` is a list of tuple where:
* 1st element is a task name,
* 2nd element is a task kwargs,
* 3rd element is a interval - it's an int value which represents seconds. Interval value means run this task 
every X-seconds.
