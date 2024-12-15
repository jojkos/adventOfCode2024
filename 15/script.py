import time

class Map:
    movement = {
        "left": (0, -1),
        "right": (0, 1),
        "up": (-1, 0),
        "down": (1, 0),
    }

    dirs = {
        "<": "left",
        ">": "right",
        "^": "up",
        "v": "down",
        "left": "<",
        "right": ">",
        "up": "^",
        "down": "v",
    }

    Empty = "."
    Robot = "@"
    Wall = "#"
    Box = "O"
    BoxLeft = "["
    BoxRight = "]"

    def __init__(self, fileName):
        with open("input.txt", "r") as file:
            input = file.readlines()

        self.map = []
        self.moves = []
        parsingMap = True

        for line in input:
            line = line.strip()

            if line == "":
                parsingMap = False
                continue

            if parsingMap:
                self.map.append([char for char in line])
            else:
                for c in line:
                    self.moves.append(c)

        self.robotPos = self.findRobotOriginalPos()

    def print(self, clear=False):
        if clear:
            print("\033[H\033[J", end="")  # Clear screen and move cursor to top
        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                print(self.map[x][y], end="")
            print()
        print("\n")

    def isInsideMapBounds(self, pos):
        (x, y) = pos
        return x >= 0 and x < len(self.map) and y >= 0 and y < len(self.map[0])

    def copyMap(self):
        return [row[:] for row in self.map]

    def findRobotOriginalPos(self):
        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                if self.map[x][y] == self.Robot:
                    return (x, y)

    def movePos(self, pos, dir):
        movement = self.movement[dir]
        return (pos[0] + movement[0], pos[1] + movement[1])

    def moveBigBox(self, posLeft, posRight, dir, newMap):
        nextPosLeft = self.movePos(posLeft, dir)
        nextPosRight = self.movePos(posRight, dir)

        newMap[nextPosLeft[0]][nextPosLeft[1]] = self.BoxLeft
        newMap[nextPosRight[0]][nextPosRight[1]] = self.BoxRight

    def moveRobotPos(self, dir):
        nextPos = self.movePos(self.robotPos, dir)

        self.map[self.robotPos[0]][self.robotPos[1]] = self.Empty
        self.map[nextPos[0]][nextPos[1]] = self.Robot
        self.robotPos = nextPos

    def getFullBoxPos(self, pos):
        if self.map[pos[0]][pos[1]] == self.BoxLeft:
            boxLeft = pos
            boxRight = (pos[0], pos[1] + 1)
        else:
            boxLeft = (pos[0], pos[1] - 1)
            boxRight = pos

        return [boxLeft, boxRight]

    def isSameBox(self, box1, box2):
        box1Left = box1[0]
        box1Right = box1[1]
        box2Left = box2[0]
        box2Right = box2[1]

        return box1Left[0] == box2Left[0] and box1Left[1] == box2Left[1] and box1Right[0] == box2Right[0] and box1Right[1] == box2Right[1]

    def isBoxInBoxes(self, box, boxes):
        for b in boxes:
            if self.isSameBox(box, b):
                return True
        return False

    def findConnectedBoxes(self, boxLeft, boxRight, dir):
        connectedBoxes = []
        stack = [[boxLeft, boxRight]]

        while len(stack) > 0:
            currentBox = stack.pop()
            connectedBoxes.append(currentBox)

            if dir == "left":
                nextPos = (currentBox[0][0], currentBox[0][1] - 1)
                nextVal = self.map[nextPos[0]][nextPos[1]]

                if nextVal == self.Wall:
                    return []
                elif nextVal == self.BoxRight:
                    stack.append([self.movePos(nextPos, dir), nextPos])
            elif dir == "right":
                nextPos = (currentBox[1][0], currentBox[1][1] + 1)
                nextVal = self.map[nextPos[0]][nextPos[1]]

                if nextVal == self.Wall:
                    return []
                elif self.map[nextPos[0]][nextPos[1]] == self.BoxLeft:
                    stack.append([nextPos, self.movePos(nextPos, dir)])
            elif dir == "up":
                for side in currentBox:
                    nextPos = (side[0] - 1, side[1])
                    nextVal = self.map[nextPos[0]][nextPos[1]]

                    if nextVal == self.Wall:
                        return []
                    elif nextVal in [self.BoxLeft, self.BoxRight]:
                        nextBox = self.getFullBoxPos(nextPos)
                        
                        if not self.isBoxInBoxes(nextBox, connectedBoxes):
                            stack.append(nextBox)
            elif dir == "down":
                for side in currentBox:
                    nextPos = (side[0] + 1, side[1])
                    nextVal = self.map[nextPos[0]][nextPos[1]]

                    if nextVal == self.Wall:
                        return []
                    elif nextVal in [self.BoxLeft, self.BoxRight]:
                        nextBox = self.getFullBoxPos(nextPos)
                        
                        if not self.isBoxInBoxes(nextBox, connectedBoxes):
                            stack.append(nextBox)
        
        return connectedBoxes

    def moveRobot2(self, dir):
        nextPos = self.movePos(self.robotPos, dir)
        nextPosVal = self.map[nextPos[0]][nextPos[1]]

        if nextPosVal == self.Wall:
            return
        elif nextPosVal == self.Empty:
            self.moveRobotPos(dir)
            return
        elif nextPosVal in [self.BoxLeft, self.BoxRight]:
            box = self.getFullBoxPos(nextPos)        
            connectedBoxes = self.findConnectedBoxes(box[0], box[1], dir)            
            mapCopy = self.copyMap()

            for i in range(len(connectedBoxes)):
                boxToMove = connectedBoxes[-i - 1]
                mapCopy[boxToMove[0][0]][boxToMove[0][1]] = self.Empty
                mapCopy[boxToMove[1][0]][boxToMove[1][1]] = self.Empty

            for i in range(len(connectedBoxes)):
                boxToMove = connectedBoxes[-i - 1]
                self.moveBigBox(boxToMove[0], boxToMove[1], dir, mapCopy)

            self.map = mapCopy

        if len(connectedBoxes) > 0:
            self.moveRobotPos(dir)

    def moveRobot(self, dir):
        # print(dir, self.robotPos)
        nextPos = self.movePos(self.robotPos, dir)
        nextPosVal = self.map[nextPos[0]][nextPos[1]]

        if nextPosVal == self.Wall:
            return
        if nextPosVal == self.Empty:
            self.moveRobotPos(dir)
            return
        if nextPosVal == self.Box:
            positionsToMove = [self.robotPos]

            while True:
                positionsToMove.append(nextPos)
                nextPos = self.movePos(nextPos, dir)
                nextPosVal = self.map[nextPos[0]][nextPos[1]]

                if nextPosVal == self.Wall:
                    return
                if nextPosVal == self.Empty:
                    break

            for i in range(len(positionsToMove)):
                posToMove = positionsToMove[-i - 1]
                valToMove = self.map[posToMove[0]][posToMove[1]]
                nextPos = self.movePos(posToMove, dir)

                if valToMove == self.Robot:
                    self.robotPos = (nextPos[0], nextPos[1])

                self.map[nextPos[0]][nextPos[1]] = self.map[posToMove[0]][posToMove[1]]
                self.map[posToMove[0]][posToMove[1]] = self.Empty

    def evaluate(self):
        result = 0

        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                if self.map[x][y] == self.Box:
                    result += x * 100 + y
        print(result)

    def evaluate2(self):
        result = 0

        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                if self.map[x][y] == self.BoxLeft:
                    result += x * 100 + y
        print(result)

    def enlargeMap(self):
        newMap = []

        for x in range(len(self.map)):
            newMap.append([])
            for y in range(len(self.map[0])):
                val = self.map[x][y]
                secondVal = val

                if val == self.Box:
                    val = self.BoxLeft
                    secondVal = self.BoxRight
                elif val == self.Robot:
                    secondVal = self.Empty

                newMap[-1].append(val)
                newMap[-1].append(secondVal)

        self.robotPos = (self.robotPos[0], self.robotPos[1] * 2)
        self.map = newMap

    def solveFirst(self):        
        for move in self.moves:
            self.moveRobot(self.dirs[move])
        self.print()
        self.evaluate()

    def solveSecond(self):
        self.enlargeMap()

        i = 0

        for move in self.moves:
            self.moveRobot2(self.dirs[move])

            if i % 100 == 0:
                self.print(True)
                time.sleep(0.0001)
            i += 1
        self.print(True)
        self.evaluate2()

map = Map("input.txt")

# map.solveFirst()
map.solveSecond()