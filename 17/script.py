with open("input.txt", "r") as file:
    input = file.readlines()

a = int(input[0].split(" ")[2])
b = int(input[1].split(" ")[2])
c = int(input[2].split(" ")[2])
program = input[4].split(" ")[1].split(",")
program = [int(i) for i in program]

pointer = 0
output = ""


def getComboOperandValue(operand):
    if operand <= 3:
        return operand
    elif operand == 4:
        return a
    elif operand == 5:
        return b
    elif operand == 6:
        return c


def adv(operand, reverse):
    global a, b, c, pointer

    if reverse:
        a = a * pow(2, getComboOperandValue(operand))
        return

    a = a // pow(2, getComboOperandValue(operand))


def bxl(operand, reverse):
    global a, b, c, pointer

    if reverse:
        b = b ^ operand
        return

    b = b ^ operand


def bst(operand, reverse):
    global a, b, c, pointer

    if reverse:
        # b = getComboOperandValue(operand) % 8
        return

    b = getComboOperandValue(operand) % 8


def jnz(operand, reverse):
    global a, b, c, pointer

    if reverse:
        return

    if a == 0:
        return

    pointer = operand

    return True


def bxc(operand, reverse):
    global a, b, c, pointer

    if reverse:
        b = b ^ c
        return

    b = b ^ c


def out(operand, reverse):
    global a, b, c, pointer, output, currentGoalIndex

    if reverse:
        currentGoal = goalList[currentGoalIndex]
        if output:
            output = f",{output}"
        output = f"{currentGoal}{output}"

        diff = currentGoal - (getComboOperandValue(operand) % 8)

        if operand == 4:
            a += diff
        elif operand == 5:
            b += diff
        elif operand == 6:
            c += diff

        currentGoalIndex -= 1

        return

    if output:
        output += ","

    output += str(getComboOperandValue(operand) % 8)


def bdv(operand, reverse):
    global a, b, c, pointer

    if reverse:
        b = a * pow(2, getComboOperandValue(operand))
        return

    b = a // pow(2, getComboOperandValue(operand))


def cdv(operand, reverse):
    global a, b, c, pointer

    if reverse:
        c = a * pow(2, getComboOperandValue(operand))
        return

    c = a // pow(2, getComboOperandValue(operand))


def runInstruction(instruction, operand, reverse=False):
    if instruction == 0:
        return adv(operand, reverse)
    elif instruction == 1:
        return bxl(operand, reverse)
    elif instruction == 2:
        return bst(operand, reverse)
    elif instruction == 3:
        return jnz(operand, reverse)
    elif instruction == 4:
        return bxc(operand, reverse)
    elif instruction == 5:
        return out(operand, reverse)
    elif instruction == 6:
        return bdv(operand, reverse)
    elif instruction == 7:
        return cdv(operand, reverse)


goal = ",".join(map(str, program))
# split on "," and map to int
goalList = list(map(int, goal.split(",")))
currentGoalIndex = -1


def solvePartOne():
    global pointer, a, b, c, output

    # for i in range(513):
    # a = 0
    # b = 0
    # c = 0
    # pointer = 0
    # output = ""

    while True:
        if pointer >= len(program):
            break

        instruction = program[pointer]
        operand = program[pointer + 1]

        pointerUpdated = runInstruction(instruction, operand)
        if not pointerUpdated:
            pointer += 2

    # print(i, output)
    print(output)
    # print("a:", a, "b:", b, "c:", c)


def solvePartTwo():
    global pointer, a, b, c, output
    a = 0
    b = 0
    c = 0
    output = ""
    pointer = len(program) - 2
    goalFound = False

    while True:
        if output == goal:
            goalFound = True

        instruction = program[pointer]
        operand = program[pointer + 1]
        pointerUpdated = runInstruction(instruction, operand, True)

        # print("a:", a,"b:", b,"c:", c)

        if pointer == 0 and goalFound:
            print("FOUND")
            break
        if pointer == 0:
            pointer = len(program) - 2
            continue

        if not pointerUpdated:
            pointer -= 2
        # print(output)
    print("a:", a, "b:", b, "c:", c)


def solveTwoBruteForce(initialNumber):
    global pointer, a, b, c, output

    goal = "2,4,1,3,7,5,4,1,1,3,0,3,5,5,3,0"
    goals = goal.split(",")
    match = 1
    i = 0

    while True:
        i += 1

        if len(output.split(",")) > len(goal.split(",")):
            print("TOO LONG", i, output)
            # print(output)
            break

        # if i % 1000 == 0:
        #     print(i)

        a = initialNumber
        b = 0
        c = 0

        pointer = 0
        output = ""

        while True:
            if pointer >= len(program):
                break

            instruction = program[pointer]
            operand = program[pointer + 1]

            pointerUpdated = runInstruction(instruction, operand)
            if not pointerUpdated:
                pointer += 2
        outputs = output.split(",")

        goalMatch = ",".join(goals[-1 * match :])
        outputMatch = ",".join(outputs[-1 * match :])

        if output == goal:
            print("FOUND", output)
            print(initialNumber)
            exit()

        if goalMatch == outputMatch:
            print("MATCH", output)
            match += 1
            if i == 0:
                initialNumber += 1
            else:
                initialNumber = initialNumber * 8
        else:
            # print(output)
            initialNumber += 1


# solvePartOne()
solveTwoBruteForce(a)
# solvePartTwo()


# bst(4, True)
# bxl(3, True)
# cdv(5, True)
# bxc(1, True)
# bxl(3, True)
# adv(3, True)
# out(5, True)
# jnz(0, True)
