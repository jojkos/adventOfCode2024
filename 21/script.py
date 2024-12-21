class Keypad:
    dirs = {
        "<": (0, -1),
        ">": (0, 1),
        "^": (-1, 0),
        "v": (1, 0),
    }
    numericKeypad = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        [None, "0", "A"],
    ]
    arrowKeypad = [[None, "^", "A"], ["<", "v", ">"]]

    def __init__(self):
        with open("input.txt", "r") as file:
            input = file.readlines()
            # remove newline characters
            input = [line.strip() for line in input]
            self.codes = input

    def findPresses(self, startPos, endPos, reverse = False):
        # manhattan distance
        x = endPos[0] - startPos[0]
        y = endPos[1] - startPos[1]

        xChar = "^" if x < 0 else "v"
        yChar = "<" if y < 0 else ">"

        if reverse:
            return abs(y) * yChar + abs(x) * xChar
        else:
            return abs(x) * xChar + abs(y) * yChar

    def getCharPosInPad(self, char, pad):
        for x in range(len(pad)):
            for y in range(len(pad[x])):
                if pad[x][y] == char:
                    return (x, y)
        return None

    def pressPad(self, pad, code, wrongPos):
        start = self.getCharPosInPad("A", pad)
        result = ""

        for char in code:
            end = self.getCharPosInPad(char, pad)
            presses = self.findPresses(start, end)

            wrongWay = False
            nextPos = start
            for press in presses:
                movement = self.dirs[press]
                nextPos = (nextPos[0] + movement[0], nextPos[1] + movement[1])
                
                if nextPos == wrongPos:
                    # print("wrongWay:", start, end, presses, movement, nextPos)
                    wrongWay = True
                    break
            if wrongWay:
                presses = self.findPresses(start, end, True)
                # print("correct:", start, end, presses)

            start = end
            result += presses + "A"

        return result

    def pressNumericPad(self, code):
        return self.pressPad(self.numericKeypad, code, ((3, 0)))

    def pressArrowPad(self, code):
        return self.pressPad(self.arrowKeypad, code, (0, 0))

keypad = Keypad()

sum = 0
for code in keypad.codes:
    numericPart = int(code.replace("A", ""))
    firstLevel = keypad.pressNumericPad(code)
    secondLevel = keypad.pressArrowPad(firstLevel)
    thirdLevel = keypad.pressArrowPad(secondLevel)

    sum += numericPart * len(thirdLevel)
    
    print(len(thirdLevel), numericPart)
    # print(code, thirdLevel)
    # print(code)
    # print(firstLevel)
    # print(secondLevel)
    # print(thirdLevel)
    
print(sum)

# res = keypad.pressNumericPad("379A")
# print(res)
# res = keypad.pressArrowPad("^A^^<<A>>AvvvA")
# print(len(res))
# print(res)