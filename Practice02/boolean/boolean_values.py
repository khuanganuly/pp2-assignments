#The bool() function allows you to evaluate any value, and give you True or False in return,
print(bool("Hello"))
print(bool(15))

x = "Hello"
y = 15

print(bool(x))
print(bool(y))


#Most Values are True
"""
Any string is True, except empty strings.

Any number is True, except 0.

Any list, tuple, set, and dictionary are True, except empty ones.
"""
#true values
bool("abc")
bool(123)
bool(["apple", "cherry", "banana"])

#false values 
bool(False)
bool(None)
bool(0)
bool("")
bool(())
bool([])
bool({})

class myclass():
  def __len__(self):
    return 0

myobj = myclass()
print(bool(myobj))



def myFunction() :
  return True

print(myFunction())


def myFunction() :
  return True

if myFunction():
  print("YES!")
else:
  print("NO!")



x = 200
print(isinstance(x, int))