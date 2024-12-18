import time
import heapq


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
    }

    Empty = "."
    Wall = "#"

    def __init__(self, width, height, count):
        with open("input.txt", "r") as file:
            input = file.readlines()
            # remove new line
            input = [x.strip() for x in input]

        self.blocks = []

        for block in input:
            y, x = block.split(",")
            self.blocks.append((int(x), int(y)))

        self.map = []

        for x in range(width):
            self.map.append([self.Empty] * height)

        for i in range(count):
            (x, y) = self.blocks[i]
            self.map[x][y] = self.Wall  

    def print(self, currentPos=None, currentDir=None, clear=False):
        if clear:
            print("\033[H\033[J", end="")  # Clear screen and move cursor to top
            time.sleep(0.1)
        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                if currentPos is not None and x == currentPos[0] and y == currentPos[1]:
                    print(currentDir, end="")
                else:
                    print(self.map[x][y], end="")
            print()
        print("\r")

    def isInsideMapBounds(self, pos):
        (x, y) = pos
        return x >= 0 and x < len(self.map) and y >= 0 and y < len(self.map[0])

    def copyMap(self):
        return [row[:] for row in self.map]

    def turnRight(self, dir):
        if dir == "<":
            return "^"
        elif dir == "^":
            return ">"
        elif dir == ">":
            return "v"
        elif dir == "v":
            return "<"

    def turnLeft(self, dir):
        if dir == "<":
            return "v"
        elif dir == "v":
            return ">"
        elif dir == ">":
            return "^"
        elif dir == "^":
            return "<"

    def movePos(self, pos, dir):
        orientation = self.dirs[dir]
        return (
            pos[0] + self.movement[orientation][0],
            pos[1] + self.movement[orientation][1],
        )

    def getDistance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def findPath(self, startPos, endPos):
        stack = []

        heapq.heappush(
            stack, (0, startPos, 0, [startPos])
        )  # priority, pos, dir, score, path

        minScore = None
        visited = {}

        while len(stack) > 0:
            prio, pos, score, path = heapq.heappop(stack)

            if pos == endPos:
                if minScore is None or score < minScore:
                    minScore = score
                # print("found:", score, minScore)
                # break
                return path + [pos]

            key = f"{pos[0]}_{pos[1]}"
            distanceToEnd = self.getDistance(pos, endPos)

            if key in visited:
                continue
            else:
                visited[key] = distanceToEnd

            if minScore is not None and score > minScore:
                continue

            # self.print(pos, dir, True)

            nextChoices = []

            for dir in self.dirs:
                nextPos = self.movePos(pos, dir)
                nextScore = score + 1

                if (
                    self.isInsideMapBounds(nextPos)
                    and self.map[nextPos[0]][nextPos[1]] != self.Wall
                ):
                    # manhatan distance from nextPos to endPos
                    dist = self.getDistance(nextPos, endPos)

                    heapq.heappush(
                        stack,
                        (dist + nextScore, nextPos, nextScore, path + [pos]),
                    )

        return minScore

# size = 7
# count = 12
size = 71
count = 1024
map = Map(size, size, count)
# map.print()

path = map.findPath((0, 0), (size - 1, size - 1))
res = len(path) - 2

remaningBlocks = map.blocks[res:]

print(len(remaningBlocks))

# i = count 
# while True:
#     print(i)
#     (x,y) = map.blocks[i]
#     map.map[x][y] = map.Wall
    
#     res = map.findPath((0, 0), (size - 1, size - 1))
    
#     if res is None:
#         block = map.blocks[i]
#         print(f"{i}: {block[1]},{block[0]}")
#         break
#     i += 1
# map.print()

# # zkusit binary search