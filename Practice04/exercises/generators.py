#1
def square_generator(n):
   for i in range(n + 1):
    yield i * i


for v in square_generator(5):
    print(v)
    



    

#2
def even_numbers(n):
    for x in range(n + 1):
        if x % 2 == 0:
            yield x

n = int(input())
print(','.join(str(num) for num in even_numbers(n)))







#3
def divisible_by_3_and_4(n):
    for x in range(n+1):
        if x % 3  == 0 and x % 4 == 0:
            yield x

for num in divisible_by_3_and_4(50):
    print(num)





#4
def squares(a, b):
    for x in range(a, b + 1):
        yield x * x

for num in squares(2,5):
    print(num)






#5
def downcount(n):
    for x in range(n, -1, -1):
        yield x

for num in downcount(5):
    print(num)