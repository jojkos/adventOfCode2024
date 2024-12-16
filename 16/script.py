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
    Start = "S"
    End = "E"
    ScoreRotate = 1000
    ScoreMove = 1

    def __init__(self, fileName):
        with open("input.txt", "r") as file:
            input = file.readlines()

        self.map = []

        for line in input:
            self.map.append([char for char in line.strip()])

        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                if self.map[x][y] == "S":
                    self.startPos = (x, y)
                elif self.map[x][y] == "E":
                    self.endPos = (x, y)

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

    def findPath(self, startPos, dir, endPos):
        stack = []

        heapq.heappush(stack, (0, startPos, dir, 0))  # priority, pos, dir, score

        minScore = None
        i = 0
        visited = {}

        while len(stack) > 0:
            prio, pos, dir, score = heapq.heappop(stack)

            if pos == endPos:
                if minScore is None or score < minScore:
                    minScore = score

                print(score, minScore)

            key = f"{pos[0]}_{pos[1]}"

            if key in visited:
                continue

            if minScore is not None and score > minScore:
                continue

            visited[key] = True

            # self.print(pos, dir, True)

            nextChoices = []

            rightDir = self.turnRight(dir)
            leftDir = self.turnLeft(dir)

            nextChoices.append(
                {"pos": self.movePos(pos, dir), "dir": dir, "score": self.ScoreMove}
            )
            nextChoices.append(
                {
                    "pos": self.movePos(pos, rightDir),
                    "dir": rightDir,
                    "score": self.ScoreRotate + self.ScoreMove,
                }
            )
            nextChoices.append(
                {
                    "pos": self.movePos(pos, leftDir),
                    "dir": leftDir,
                    "score": self.ScoreRotate + self.ScoreMove,
                }
            )

            for choice in nextChoices:
                nextPos = choice["pos"]
                nextDir = choice["dir"]
                nextScore = choice["score"] + score

                if (
                    self.isInsideMapBounds(nextPos)
                    and self.map[nextPos[0]][nextPos[1]] != self.Wall
                ):
                    # manhatan distance from nextPos to endPos
                    dist = abs(nextPos[0] - endPos[0]) + abs(nextPos[1] - endPos[1])

                    heapq.heappush(
                        stack, (dist + nextScore, nextPos, nextDir, nextScore)
                    )

        return minScore


map = Map("input.txt")
# map.print()

res = map.findPath(map.startPos, ">", map.endPos)
print(res)
