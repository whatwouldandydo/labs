from decorators import do_twice

@do_twice
def greeting():
    print("Hello")

greeting()
print()
