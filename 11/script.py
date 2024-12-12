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
    Max = 10
    print(input)

    while count < Max:
        input = blink(input)
        count += 1
        print(count, len(input), input)

    print(len(input))
    

def solveSecond(input):
    count = 0
    max = 75
    cache = {}

    for val in input:
        if val not in cache:
            cache[val] = 1
        else:
            cache[val] += 1

    while count <= max:
        newCache = {}
        # reduce the values in cache into sum
        sum = 0
        for val in cache:
            sum += cache[val]
        print(count, sum)

        
        for val in cache:
            occurence = cache[val]
            
            newVals = applyRule(val)

            for v in newVals:
                if v not in newCache:
                    newCache[v] = occurence
                else:
                    newCache[v] += occurence
        
        cache = newCache
        count += 1


# solveFirst(input)

solveSecond(input)