import re


# 1) Match a string that has an 'a' followed by zero or more 'b'

def task1(text):
    pattern = r"ab*"
    return bool(re.fullmatch(pattern, text))

print("1)", task1("a"))        # True
print("1)", task1("abbb"))     # True
print("1)", task1("ac"))       # False



# 2) Match a string that has an 'a' followed by two to three 'b'

def task2(text):
    pattern = r"ab{2,3}"
    return bool(re.fullmatch(pattern, text))

print("2)", task2("abb"))      # True
print("2)", task2("abbb"))     # True
print("2)", task2("abbbb"))    # False



# 3) Find sequences of lowercase letters joined with an underscore

def task3(text):
    pattern = r"[a-z]+_[a-z]+"
    return re.findall(pattern, text)

print("3)", task3("hello_world test_string Example_Test"))



# 4) Find sequences of one uppercase letter followed by lowercase letters

def task4(text):
    pattern = r"[A-Z][a-z]+"
    return re.findall(pattern, text)

print("4)", task4("Hello world Python Is Good"))



# 5) Match a string that has an 'a' followed by anything, ending in 'b'

def task5(text):
    pattern = r"a.*b"
    return bool(re.fullmatch(pattern, text))

print("5)", task5("axxxb"))    # True
print("5)", task5("ab"))       # True
print("5)", task5("axxx"))     # False



# 6) Replace all occurrences of space, comma, or dot with a colon

def task6(text):
    return re.sub(r"[ ,\.]", ":", text)

print("6)", task6("Hello, world. Python is cool"))



# 7) Convert snake_case string to camelCase string

def task7(text):
    return re.sub(r"_([a-z])", lambda m: m.group(1).upper(), text)

print("7)", task7("hello_world_python"))



# 8) Split a string at uppercase letters

def task8(text):
    return re.split(r"(?=[A-Z])", text)

print("8)", task8("HelloWorldPython"))



# 9) Insert spaces between words starting with capital letters

def task9(text):
    return re.sub(r"([A-Z])", r" \1", text).strip()

print("9)", task9("HelloWorldPython"))



# 10) Convert a given camelCase string to snake_case

def task10(text):
    return re.sub(r"([A-Z])", r"_\1", text).lower()

print("10)", task10("helloWorldPython"))