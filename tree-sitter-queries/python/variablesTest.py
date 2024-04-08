import math
from math import sqrt
import math as m
from math import *
from math import sqrt as square_root
import my_package.my_module
from my_package.my_module import my_function

def outer_func():
    nonlocal_var, v2 = "I'm a nonlocal variable"

    def inner_func():
        nonlocal nonlocal_var
        nonlocal_var = "I've been changed in the inner function"
        print(nonlocal_var)

class MyClass:
    static_var = "I'm a class static variable"

    @staticmethod
    def test_func():
        print(MyClass.static_var)

class MyClass:
    def __init__(self):
        self.member_var = "I'm a class member variable"

    def test_func(self):
        print(self.member_var)

def test_func(param: str, param2: str = "", param3 = 10):
    print("I'm a function parameter: ", param)

def test_func():
    local_var = "I'm a local variable"
    print(local_var)

global_var = "I'm a global variable"
