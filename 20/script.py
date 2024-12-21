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

    oppositeDirs = {
        "<": ">",
        ">": "<",
        "^": "v",
        "v": "^",
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

    def getDistance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def findPath(self, startPos, endPos, initialIgnoreWalls=0, initialVisited = {}, findAll = False):
        stack = []

        heapq.heappush(
            stack, (0, startPos, 0, [startPos], [self.Start], initialIgnoreWalls)
        )  # priority, pos, score, path, dir, ignoreWalls

        minScore = None
        visited = initialVisited.copy()
        allPaths = []

        while len(stack) > 0:
            prio, pos, score, path, dir, ignoreWalls = heapq.heappop(stack)

            if pos == endPos:
                if minScore is None or score < minScore:
                    minScore = score
                # print("found:", score, minScore)
                # break
                if not findAll:
                    return {
                        "path": path,
                        "dirs": dir,
                        "len" : score
                    }
                else:
                    allPaths.append({
                        "path": path,
                        "dirs": dir,
                        "len" : score
                    })

            key = f"{pos[0]}_{pos[1]}"
            distanceToEnd = self.getDistance(pos, endPos)

            if key in visited:
                continue
            else:
                visited[key] = distanceToEnd

            if minScore is not None and score > minScore:
                continue

            # self.print(pos, dir, True)

            for d in self.dirs:
                nextPos = self.movePos(pos, d)
                nextScore = score + 1

                if self.isInsideMapBounds(nextPos) and (
                    self.map[nextPos[0]][nextPos[1]] != self.Wall or ignoreWalls > 0
                ):
                    # manhatan distance from nextPos to endPos
                    dist = self.getDistance(nextPos, endPos)

                    heapq.heappush(
                        stack,
                        (
                            dist + nextScore,
                            nextPos,
                            nextScore,
                            path + [nextPos],
                            dir + [d],
                            ignoreWalls - 1,
                        ),
                    )

        return allPaths

    def findAllCheats(self, path, dirs):
        cheats = []
        visited = {}

        for i in range(len(path)):
            pos = path[i]
            dir = dirs[i]
            key = f"{pos[0]}_{pos[1]}"
            visited[key] = True

            if self.map[pos[0]][pos[1]] == self.End:
                continue

            for nextDir in self.dirs:
                if dir == nextDir or dir == self.oppositeDirs[nextDir]:
                    continue
                nextPos = self.movePos(pos, nextDir)
                nextNextPos = self.movePos(nextPos, nextDir)

                bothPos = [nextPos, nextNextPos]
                # sort both pos so we can use it as a key, primarily over pos[0] and secondary pos[1]
                bothPos.sort(key=lambda x: (x[0], x[1]))
                # key = f"{bothPos[0][0]}_{bothPos[0][1]}_{bothPos[1][0]}_{bothPos[1][1]}"

                if not self.isInsideMapBounds(nextNextPos):
                    continue

                nextPosVal = self.map[nextPos[0]][nextPos[1]]
                nextNextPosVal = self.map[nextNextPos[0]][nextNextPos[1]]

                if nextPosVal != self.Wall and nextNextPosVal != self.Wall:
                    continue

                emptyFound = False

                for d in self.dirs:
                    if d == self.oppositeDirs[nextDir]:
                        continue

                    emptyPos = self.movePos(nextNextPos, d)

                    if self.map[emptyPos[0]][emptyPos[1]] == self.Empty:
                        emptyKey = f"{emptyPos[0]}_{emptyPos[1]}"

                        if emptyKey in visited:
                            continue

                        emptyFound = True
                        break

                if emptyFound:
                    visited[key] = True
                    cheats.append(bothPos)

        return cheats

    def findAllCheatLengths(self, path, dirs, originalLen):
        visited = {}
        lengths = {}
        originalMap = map.copyMap()
        cheatLen = 1

        for i in range(len(path)):
            pos = path[i]
            key = f"{pos[0]}_{pos[1]}"

            if self.map[pos[0]][pos[1]] == self.End:
                break
            
            if pos == (7,9):
                print("TEST")

            for d in self.dirs:
                nextPos = self.movePos(pos, d)
                nextPosVal = self.map[nextPos[0]][nextPos[1]]

                if nextPosVal == self.Wall:
                    map.map = originalMap
                    map.map = map.copyMap()

                    self.map[nextPos[0]][nextPos[1]] = map.Empty

                    res = self.findPath(nextPos, self.endPos, cheatLen, visited, True)

                    for r in res:
                        resLenPath = r["len"]
                        fullLen = resLenPath + i + 1
                        visited[key] = True

                        if fullLen < originalLen:
                            diff = originalLen - fullLen

                            if diff not in lengths:
                                lengths[diff] = 0
                            lengths[diff] += 1

        return lengths

    def removeOnWallAtATime(self, walls, originalLen):
        lengths = {}
        # walls = []

        # for x in range(len(self.map)):
        #     for y in range(len(self.map[0])):
        #         if self.map[x][y] == self.Wall:
        #             walls.append((x, y))

        originalMap = map.copyMap()
        print(len(walls))
        i = 0
        for wall in walls:
            i += 1
            print(i)
            map.map = originalMap
            map.map = map.copyMap()

            map.map[wall[0]][wall[1]] = map.Empty

            res = map.findPath(map.startPos, map.endPos)
            resLen = len(res["path"])

            if resLen < originalLen or True:
                diff = originalLen - resLen

                if diff not in lengths:
                    lengths[diff] = 0
                lengths[diff] += 1

        return lengths

    def getWallsAlongThePath(self, path):
        visited = {}
        walls = []

        for i in range(len(path)):
            pos = path[i]
            if self.map[pos[0]][pos[1]] == self.End:
                break

            for d in self.dirs:
                nextPos = self.movePos(pos, d)
                key = f"{nextPos[0]}_{nextPos[1]}"
                if key in visited:
                    continue

                if self.map[nextPos[0]][nextPos[1]] == self.Wall:
                    visited[key] = True
                    walls.append(nextPos)

        return walls


map = Map("input.txt")
# map.print()

res = map.findPath(map.startPos, map.endPos)
originalLen = res["len"]

print("original len:", originalLen)

# print the path in map
# for i in range(len(res["path"])):
#     pos = res["path"][i]
#     dir = res["dirs"][i]
#     map.map[pos[0]][pos[1]] = dir
# map.print()

lengths = map.findAllCheatLengths(res["path"], res["dirs"], originalLen)
# walls = map.getWallsAlongThePath(res["path"])
# print(len(walls))
# lengths = map.removeOnWallAtATime(walls, originalLen)

lengthsArray = []
for length in lengths:
    if length >= originalLen:
        continue
    lengthsArray.append((length, lengths[length]))

lengthsArray.sort(key=lambda x: x[0])

print(lengthsArray)

sum = 0
for length in lengthsArray:
    if length[0] >= 100:
        sum += length[1]

print(sum)

# cheats = map.findAllCheats(res["path"], res["dirs"])

# originalMap = map.copyMap()

# lengths = {}

# for cheat in cheats:
#     # map.print()
#     map.map = originalMap
#     map.map = map.copyMap()
#     # print(cheat)

#     for pos in cheat:
#         map.map[pos[0]][pos[1]] = map.Empty

#     # map.print()

#     res = map.findPath(map.startPos, map.endPos)
#     currentLen = len(res["path"])

#     if currentLen not in lengths:
#         lengths[currentLen] = 0

#     lengths[currentLen] += 1

#     if originalLen - currentLen == 36:
#         print(cheat)
