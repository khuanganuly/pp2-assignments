"""
Python is an object oriented programming language.

Almost everything in Python is an object, with its properties and methods.

A Class is like an object constructor, or a "blueprint" for creating objects.
"""


class MyClass:   #create a class
  x = 5


p1 = MyClass()   #creating object
print(p1.x)

del p1   #delete object


p1 = MyClass() #multiple object
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)



class Person:
  pass
