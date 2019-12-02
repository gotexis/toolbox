import timeit
import functools


def repeat_and_time(times):  # what the decorator argument will be

    def actual_decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            start = timeit.default_timer()                                       # start timer

            for i in range(times):                                               # execute function
                func(*args, **kwargs)

            end = timeit.default_timer()                                         # end timer

            print(f"The running time for {func.__name__} is {end - start}")      # print report

        return wrapper

    return actual_decorator

