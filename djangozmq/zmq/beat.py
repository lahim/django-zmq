import time
import logging

from djangozmq import settings, objects

logger = logging.getLogger(settings.LOGGER_NAME)


def _load_tasks() -> list:
    tasks = []

    for periodic_task in settings.PERIODIC_TASKS:
        task_name, kwargs, interval = periodic_task
        tasks.append(objects.PeriodicTask(task_name, kwargs, interval))

    return tasks


# ToDo: run beat on more than one process
def run():
    tasks = _load_tasks()

    log_tasks = '\n' + '*' * 120
    log_tasks += '\n>>>>>> DEFINED PERIODIC TASKS <<<<<<\n'
    for t in tasks:
        log_tasks += f'\n{t.name} (run every: {t.interval} seconds)'
    log_tasks += '\n\n' + '*' * 120 + '\n'
    logger.info(log_tasks)

    s_time = time.time()
    uptime = 0
    while True:
        logger.debug(f'> uptime: {uptime} seconds')
        for task in tasks:
            if uptime > 0 and uptime % task.interval == 0:
                logger.info(f'Task: {task.name} is running... | uptime: {uptime}')
                task.call()

        time.sleep(settings.BEAT_SLEEP_TIME)
        uptime = int(time.time() - s_time)


if __name__ == '__main__':
    run()
