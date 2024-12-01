import functools

with open("input.txt", "r") as file:
    data = file.readlines()

left = []
right = []

for line in data:
    l,r = line.split()
    left.append(int(l.strip()))
    right.append(int(r.strip()))

left.sort()
right.sort()

final = []

for i in range(len(left)):
    diff = abs(left[i] - right[i])
    final.append(diff)

part_one = functools.reduce(lambda x, y: x + y, final)

print(part_one)

similarity_score = 0

for i in left:
    found = 0
    for j in right:
        if i == j:
            found += 1
    similarity_score += found * i


print(similarity_score)