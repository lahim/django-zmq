def foo_task():
    print('Foo task is running...')
    print('Foo task completed.')
    return True


def sum_task(arg_1: int, arg_2: int):
    print('Sum task is running...')
    result = arg_1 + arg_2
    print('Sum task completed.')
    return result
