with open("input.txt", "r") as file:
    input = file.readlines()[0].strip()

def printData(data):
    for val in data:
        if val["type"] == "data":
            print(str(val["id"]) * val["length"], end="")
        else:
            print("." * val["length"], end="")
    print()

data = []
isEmptySpace = False
id = 0

for val in input:
    number = int(val)

    if not isEmptySpace:
        data.append({
            "type": "data",
            "length": number,
            "id": id
        })
        id += 1
    else:
        data.append({
            "type": "empty",
            "length": number,
        })

    isEmptySpace = not isEmptySpace


data.append({
    "type": "empty",
    "length": 0
})

def mergeLastEmpty(data):
    if data[-1]["type"] == "empty" and data[-2]["type"] == "empty":
        data[-1]["length"] += data[-2]["length"]
        data.pop(-2)

def getChecksum(data):
    sum = 0
    i = 0

    for val in data:
        if val["type"] == "data":        
            for j in range(i, i + val["length"]):                
                sum += val["id"] * j

        i += val["length"]
    
    return sum

def solve_one():
    currentEmptyIndex = 1
    lastEmpty = data[-1]

    i = 0

    while True:
        if currentEmptyIndex == len(data) - 1:
            break

        currentEmpty = data[currentEmptyIndex]
        lastData = data[-2]
        lastDataLength = lastData["length"]
        currentEmptyLength = currentEmpty["length"]

        if lastDataLength == currentEmptyLength:
            data[currentEmptyIndex] = lastData
            lastEmpty["length"] += lastDataLength
            currentEmptyIndex += 2
            data.pop(-2)

        elif lastDataLength > currentEmptyLength:
            data[currentEmptyIndex] = {
                "type": "data",
                "length": currentEmptyLength,
                "id": lastData["id"]
            }
            lastData["length"] -= currentEmptyLength
            lastEmpty["length"] += currentEmptyLength
            currentEmptyIndex += 2
        elif lastDataLength < currentEmptyLength:
            # insert lastData into currentEmptyIndex - 1
            data.insert(currentEmptyIndex, lastData)
            currentEmptyIndex += 1
            currentEmpty["length"] -= lastDataLength
            lastEmpty["length"] += lastDataLength
            # remove lastData
            data.pop(-2)
            
        mergeLastEmpty(data)
        # printData(data)

    # printData(data)
    print(getChecksum(data))

def findFittingEmpty(data, length):
    for i in range(len(data)):
        if data[i]["type"] == "empty" and data[i]["length"] >= length:
            return i
        
    return -1

def findPreviousData(data, index):
    for i in range(index, -1, -1):
        if data[i]["type"] == "data":
            if i != index:
                return i

    return -1

def solve_two():
    currentDataIndex = len(data) - 2
    # printData(data)

    while True:
        currentData = data[currentDataIndex]
        fittingEmptyIndex = findFittingEmpty(data, currentData["length"])

        # print(currentData, fittingEmptyIndex)

        if fittingEmptyIndex >= 0 and fittingEmptyIndex < currentDataIndex:
            currentDataLength = currentData["length"]
            fittingEmpty = data[fittingEmptyIndex]
            fittingEmpty["length"] -= currentDataLength

            if data[currentDataIndex + 1]["type"] == "empty":
                data[currentDataIndex + 1]["length"] += currentDataLength            
                data.pop(currentDataIndex)
            else:
                data[currentDataIndex] = {"type": "empty", "length": currentDataLength}
            data.insert(fittingEmptyIndex, currentData)

        currentDataIndex = findPreviousData(data, currentDataIndex)

        mergeLastEmpty(data)

        if currentDataIndex <= 0:
            break
    print(getChecksum(data))

# solve_one()
solve_two()
