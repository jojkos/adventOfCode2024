with open("input.txt", "r") as file:
    data = file.readlines()

# remove \n from each line
data = [line.strip() for line in data]

values = {}

for line in data:
    result, numbers = line.split(":")
    
    values[result] = numbers.strip().split(" ")
    # map to int
    values[result] = list(map(int, values[result]))

operations = ["+", "*"]

def evaluate(values, result):
    leftVal = values.pop(0)
    rightVal = values.pop(0)
    
    for op in operations:
        if op == "+":
            currentRes  = leftVal + rightVal
        elif op == "*":
            currentRes  = leftVal * rightVal
        elif op == "||":
            currentRes  = int(str(leftVal) + str(rightVal))
        
        if len(values) == 0:
            # print(currentRes)
            if int(currentRes) == int(result):
                return True
        else:
            newValues = values.copy()
            newValues.insert(0, currentRes)
            
            if evaluate(newValues, result):
                return True
    
    return False

res_one = 0

for key in values:
    found = evaluate(values[key], key)

    if found:
        res_one += int(key)

print(res_one)

res_two = 0

operations.append("||")

for key in values:
    found = evaluate(values[key], key)

    if found:
        res_one += int(key)

print(res_one)