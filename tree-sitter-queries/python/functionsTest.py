def simple_function():
    print("Hello, World!")

def greet(name):
    print("Hello, " + name + "!")

def greet(name="World"):
    print("Hello, " + name + "!")

def sum_numbers(*args):
    total = 0
    for num in args:
        total += num
    return total

def print_kwargs(**kwargs):
    for key, value in kwargs.items():
        print(key + ": " + str(value))

def greet(name, greeting="Hello"):
    print(greeting + ", " + name + "!")

def square(x):
    return x * x

def divide(a, b):
    return a // b, a % b

def outer_function():
    def inner_function():
        print("I'm inside the outer function!")

    inner_function()

def apply_function(func, x):
    return func(x)

def my_decorator(func):
    def wrapper():
        print("Before the function is called.")
        func()
        print("After the function is called.")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

class MyClass:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello, {self.name}!")

class MyClass:
    counter = 0

    def __init__(self, name):
        self.name = name
        MyClass.counter += 1

    @classmethod
    def get_counter(cls):
        return cls.counter

class MyClass:
    @staticmethod
    def is_even(num):
        return num % 2 == 0

