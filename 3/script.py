import re

with open("input.txt", "r") as file:
    data = file.readlines()

# regex that will match mul(1-3 digits, 1-3digits) in all lines
patternMul = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)",re.MULTILINE)

result1 = 0

# find all matches in the data
matches = [patternMul.findall(line) for line in data]

for line in matches:
    for match in line:
        # get the two numbers from the match
        a, b = match
        result1 += int(a) * int(b)

print(result1)

# regex matchin "do()"
patternDo = re.compile(r"do\(\)")
#regex matching "don't()"
patternDont = re.compile(r"don't\(\)")

doMul = True
result2 = 0

for line in data:
    commands = {}
    for match in re.finditer(patternMul, line):
        # print(match.groups(), match.start())
        commands[match.start()] = {
            "command": "mul",
            "value": int(match.groups()[0]) * int(match.groups()[1])
        }
    for match in re.finditer(patternDo, line):
        commands[match.start()] = {
            "command": "do"
        }
    for match in re.finditer(patternDont, line):
        commands[match.start()] = {
            "command": "dont"
        }

    commandIndexes = sorted(list(commands.keys()))

    for index in commandIndexes:
        command = commands[index]

        if command["command"] == "do":
            doMul = True
        elif command["command"] == "dont":
            doMul = False
        elif command["command"] == "mul":
            if doMul:
                result2 += command["value"]
    
print(result2)