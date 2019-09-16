import json
import importlib


class TaskMixin:
    def set_kwargs(self, kwargs: dict):
        self.kwargs = json.dumps(kwargs)

    def get_kwargs(self):
        return json.loads(self.kwargs) if self.kwargs else {}

    def set_result(self, result):
        if not result:
            return

        if not isinstance(result, dict):
            result = {'result': result}

        self.result = json.dumps(result)

    def get_result(self):
        return json.loads(self.result) if self.result else {}

    def get_module(self):
        return '.'.join(self.name.split('.')[:-1])

    def get_function(self):
        return self.name.split('.')[-1]

    def on_error(self, err):
        raise NotImplementedError()

    def on_success(self, result):
        raise NotImplementedError()

    def post_call(self):
        raise NotImplementedError()

    def call(self):
        try:
            module = importlib.import_module(self.get_module())
            task_fun = getattr(module, self.get_function())
            result = task_fun(**self.get_kwargs())
        except Exception as err:
            self.on_error(err)
        else:
            self.on_success(result)

        self.post_call()
