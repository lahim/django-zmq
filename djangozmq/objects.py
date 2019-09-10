import logging

from . import mixins

logger = logging.getLogger(__name__)


class PeriodicTask(mixins.TaskMixin):
    def __init__(self, name, kwargs: dict, interval: int):
        self.name = name
        self.kwargs = kwargs
        self.interval = interval

    def set_kwargs(self, kwargs: dict):
        self.kwargs = kwargs

    def get_kwargs(self):
        return self.kwargs if self.kwargs else {}

    def on_error(self, err):
        logger.warning(f'Task: {self.name} was not finished - something went wrong. Details: {str(err)}')

    def on_success(self, result):
        logger.info(f'Task: {self.name} was finished with success.')

    def post_call(self):
        pass
