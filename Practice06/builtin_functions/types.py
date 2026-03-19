# type checking examples
value1 = "123"
value2 = 45
value3 = 3.14
value4 = [1, 2, 3]

print(type(value1))
print(type(value2))
print(type(value3))
print(type(value4))


print(isinstance(value1, str))
print(isinstance(value2, int))
print(isinstance(value3, float))
print(isinstance(value4, list))


# type conversion examples

a = "100"
b = int(a)
print(b, type(b))


c = float(b)
print(c, type(c))


d = str(b)
print(d, type(d))

# string to list
word = "python"
letters = list(word)
print(letters, type(letters))