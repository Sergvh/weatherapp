import time


def slow_one_second(func):
    """ Waits one second before calling function."""

    def wrapper(*args, **kwargs):
        time.sleep(1)
        return func(*args, **kwargs)

    return wrapper


def slow_down(sec=1):
    def one_moment(func):
        """ Waits one second before calling function."""

        def wrapper(*args, **kwargs):
            time.sleep(sec)
            return func(*args, **kwargs)

        return wrapper

    return one_moment


def timer(func):
    """Print the runtime of the decorated function"""
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        run_time = time.perf_counter() - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return result
    return wrapper


def parameters_print(func):
    """Print the runtime of the decorated function"""

    def wrapper(*args, **kwargs):
        print('\n')
        print(*args, **kwargs)
        print('\n')
        return func(*args, **kwargs)
    return wrapper


@parameters_print
def hello(name='Serhii', *args, **kwargs):
    print(f'Hello {name}')


hello('Serg', 123, 'hi', None)
