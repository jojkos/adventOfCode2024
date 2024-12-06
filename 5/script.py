import math
from functools import cmp_to_key

with open("input.txt", "r") as file:
    data = file.readlines()

rules = {}
updates = []
parsingFirstPart = True

for line in data:
    if line == "\n":
        parsingFirstPart = False
        continue
    line = line.strip()
    if parsingFirstPart:
        left, right = line.split("|")

        if not left in rules:
            rules[left] = []

        rules[left].append(right)
    else:
        updates.append(line.split(","))

def findRule(left, right):
    if left not in rules:
        return None
    
    return right in rules[left]

def returnMiddleValue(update):
    middle = math.ceil(len(update) / 2) - 1
    return int(update[middle])

def customSort(a, b):
    if findRule(a, b):
        return -1
    if findRule(b, a):
        return 1
    return 0

res_one = 0
res_two = 0

for update in updates:
    found = True

    for i in range(len(update) - 1):
        left = update[i]
        right = update[i + 1]

        rule = findRule(left, right)

        if not rule:
            found = False

            sortedUpdate = sorted(update, key=cmp_to_key(customSort))
            res_two += returnMiddleValue(sortedUpdate)

            break
    if found:    
        res_one += returnMiddleValue(update)

print(res_one)
print(res_two)