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


def adv(operand):
    global a, b, c, pointer
    a = a // pow(2, getComboOperandValue(operand))


def bxl(operand):
    global a, b, c, pointer
    b = b ^ operand


def bst(operand):
    global a, b, c, pointer
    b = getComboOperandValue(operand) % 8


def jnz(operand):
    global a, b, c, pointer
    if a == 0:
        return False

    pointer = operand

    return True


def bxc(operand):
    global a, b, c, pointer
    b = b ^ c


def out(operand):
    global a, b, c, pointer, output

    if output:
        output += ","

    output += str(getComboOperandValue(operand) % 8)


def bdv(operand):
    global a, b, c, pointer
    b = a // pow(2, getComboOperandValue(operand))


def cdv(operand):
    global a, b, c, pointer
    c = a // pow(2, getComboOperandValue(operand))


def runInstruction(instruction, operand):
    if instruction == 0:
        return adv(operand)
    elif instruction == 1:
        return bxl(operand)
    elif instruction == 2:
        return bst(operand)
    elif instruction == 3:
        return jnz(operand)
    elif instruction == 4:
        return bxc(operand)
    elif instruction == 5:
        return out(operand)
    elif instruction == 6:
        return bdv(operand)
    elif instruction == 7:
        return cdv(operand)

i = 0
goal = ','.join(map(str, program))
print(goal)

while True:
    # print(i)
    a = i
    b = 0
    c = 0
    pointer = 0
    output = ""

    while True:
        if pointer >= len(program):
            break

        instruction = program[pointer]
        operand = program[pointer + 1]

        # print(
        #     "pointer:, ",
        #     pointer,
        #     "instruction: ",
        #     instruction,
        #     "operand: ",
        #     operand,
        #     "a: ",
        #     a,
        #     "b: ",
        #     b,
        #     "c: ",
        #     c,
        # )

        pointerUpdated = runInstruction(instruction, operand)
        if not pointerUpdated:
            pointer += 2

    if output == goal:
        print(i)
        break

    i += 1

print(output)
