# Django-ZMQ
Simple integration ZMQ with Django.

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
    'jobmanager.tasks.send_email',
    'jobmanager.tasks.send_text_message',
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

4. Now, you can send data to the socket as presented below:
```python
import zmq 
 
ctx = zmq.Context() 
task_socket = ctx.socket(zmq.PUSH) 
task_socket.connect('tcp://127.0.0.1:5000')                                                                                                                                                                

task_socket.send_json({ 
        'task': 'jobmanager.tasks.send_text_message', 
        'kwargs': {'a': 1, 'b': 2, 'c': 3, 'd': 4}, 
    }) 

```
