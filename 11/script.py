with open("input.txt", "r") as file:
    input = file.readlines()[0].strip()
    input = [int(x) for x in input.split(" ")]

def isEven(num):
    return num % 2 == 0

def applyRule(val):
    res = []

    if val == 0:
        res.append(1)
    elif isEven(len(str(val))):
        tmp = str(val)  
        middle = len(tmp)//2
        left = tmp[:middle]
        right = tmp[middle:]
        res.append(int(left))
        res.append(int(right))
    else:
        res.append(val * 2024)

    return res

def blink(data):
    newData = []
    
    for val in data:
        newData += applyRule(val)

    return newData

def solveFirst(input):
    count = 0
    Max = 25
    print(input)

    while count < Max:
        input = blink(input)
        count += 1
        print(count, len(input))

    print(len(input))

def solveSecond(input):
    count = 0
    Max = 75
    print(input)
    res = len(input)
    # set made from input
    visited = {}


    while count < Max:
        for val in input:
            if val not in visited:
                visited[val] = []
            
            
        break
    print(visited)

    print(len(input))

# solveFirst(input)

solveSecond(input)