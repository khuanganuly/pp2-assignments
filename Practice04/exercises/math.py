#1
import math

degree = float(input("Input degree: "))
radian = degree * (math.pi / 180)

print("radian:", round(radian, 6))





#2
h = float(input("Height: "))
a = float(input("Base, first value: "))
b = float(input("Base, second value: "))

trapezoid_area = (a + b) * h * 0.5
print("Expected Output: ", trapezoid_area)



#3
n = int(input("Number of sides: "))
s = float(input("Length of a side: "))

polygon_area = (n * s * s) / (4 * math.tan(math.pi / n))
print("Area of the polygon: ", polygon_area) 




#4
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))

area = base * height

print("Expected Output:", area)


