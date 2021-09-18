from decorators import do_twice2

@do_twice2
def greet_name(name):
    print(f"Hello {name}")


greet_name("Teddy")
