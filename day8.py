import sys

width = 25
height = 6

with open("input8") as f:
    numbers = f.read().strip()

size = width * height

i = 0
result = 0
zeros = sys.maxsize
while i + size <= len(numbers):
    layer = numbers[i:i+size]
    layer_zeros = layer.count("0")
    if layer_zeros < zeros:
        zeros = layer_zeros
        result = layer.count("1") * layer.count("2")
    i += size
print(result)

result = size * ["2"]
for i in range(len(numbers)):
    index = i % size
    if result[index] == "2":
        result[index] = numbers[i]

for i in range(0, size, width):
    print("".join(result[i:i+width]).replace("0"," "))