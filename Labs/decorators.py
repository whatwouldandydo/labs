import functools
import time

def do_twice(func):
    def wrapper_do_twice():
        print("Before the function is called.")
        func()
        func()
        print("After the function is called.")
    return wrapper_do_twice


# Allow insider function to pass as many arguments
def do_twice2(func):
    def wrapper_do_twice2(*args, **kwargs):
        func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapper_do_twice2


# timer decorator
def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer


# Count down decorator
def slow_down(func):
    @functools.wraps(func)
    def wrapper_slow_down(*args, **kwargs):
        time.sleep(1)
        return func(*args, **kwargs)
    return wrapper_slow_down

# ## Without decorator ##
# def say_whee():
#     print("Whee!")

# t1 = do_twice(say_whee)
# print(t1) # <function do_twice.<locals>.wrapper_do_twice at 0x7fa830ac20d0>
# t1() # Whee!

# ## With decorator ##
# @do_twice
# def say_whee2():
#     print("Whee2!")

# say_whee2()