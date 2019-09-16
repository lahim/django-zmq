import json
import unittest
from unittest import TestCase
from unittest.mock import patch

from djangozmq import models


class TaskTestCase(TestCase):
    def setUp(self) -> None:
        pass

    @patch('djangozmq.models.Task.save')
    def test_task_status_after_execution(self, save_mock):
        task = models.Task(
            name='djangozmq.tests.simpletasks.foo_task',
            status=models.TaskStatus.QUEUED.value)

        self.assertEqual(task.status, models.TaskStatus.QUEUED.value)
        task.execute()
        self.assertEqual(task.status, models.TaskStatus.COMPLETED.value)

        save_mock.assert_called()

    @patch('djangozmq.models.Task.save')
    def test_task_result_called_without_kwargs(self, save_mock):
        task = models.Task(
            name='djangozmq.tests.simpletasks.foo_task',
            status=models.TaskStatus.QUEUED.value)
        task.execute()
        self.assertEqual(task.get_result(), {'result': True})

        save_mock.assert_called()

    @patch('djangozmq.models.Task.save')
    def test_task_result_called_with_kwargs(self, save_mock):
        task = models.Task(
            name='djangozmq.tests.simpletasks.sum_task',
            kwargs=json.dumps({'arg_1': 1., 'arg_2': 3}),
            status=models.TaskStatus.QUEUED.value)

        task.execute()
        self.assertEqual(task.get_result(), {'result': 4})

        save_mock.assert_called()

    @patch('djangozmq.models.Task.save')
    def test_execute_with_not_existing_importing_module(self, save_mock):
        task = models.Task(
            name='djangozmq.tests.simpletasks.undefined_function',
            kwargs=json.dumps({'a': True, 'b': False}),
            status=models.TaskStatus.QUEUED.value)

        task.execute()

        self.assertEqual(task.status, models.TaskStatus.FAILED.value)
        self.assertEqual(task.error, 'module \'djangozmq.tests.simpletasks\' has no attribute \'undefined_function\'')

        save_mock.assert_called()


if __name__ == '__main__':
    unittest.main()
