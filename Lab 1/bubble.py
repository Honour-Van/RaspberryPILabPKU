import random as r
data = []
for i in range(0,10):
    data.append(r.randint(0, 99))

l = len(data)

for i in range(l):
    print(data[i],end = ' ')
print()
for i in range(l):
    for j in range(l-i-1):
        if data[j+1] > data[j]:
            data[j], data[j+1] = data[j+1], data[j]

for i in range(l):
    print(data[i],end = ' ')