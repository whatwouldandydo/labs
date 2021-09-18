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