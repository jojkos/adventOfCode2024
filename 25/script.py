with open("input.txt", "r") as file:
    input = file.readlines()

Empty = "."
Filled = "#"
parsing = None

keys = []
locks = []
values = None

i = 0
for i in range(len(input)):
    line = input[i]
    line = line.strip()
    isLineBeforeEmpty = i == len(input) - 1 or input[i + 1].strip() == ""

    if line == "":
        parsing = None
        continue
    if parsing is None:
        values = [0] * len(line)
        firstChar = line[0]
        if firstChar == Empty:
            parsing = "lock"
        elif firstChar == Filled:
            parsing = "key"
        continue

    # create array of line length filled with zeros

    if not isLineBeforeEmpty:
        for i in range(len(line)):
            if line[i] == Filled:
                values[i] += 1
    else:
        if parsing == "key":
            keys.append(values)
        elif parsing == "lock":
            locks.append(values)


def testFit(key, lock):
    maxSize = 5
    for i in range(len(key)):
        if key[i] + lock[i] > maxSize:
            return False
    return True


sum = 0

for i in range(len(keys)):
    for j in range(len(locks)):
        if testFit(keys[i], locks[j]):
            sum += 1
print(sum)
