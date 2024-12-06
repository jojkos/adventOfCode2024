with open("input.txt", "r") as file:
    data = file.readlines()

map = [list(line.strip()) for line in data]


# TODO utils file
def getVal(pos, map):
    if pos[0] < 0 or pos[0] >= len(map):
        return None
    if pos[1] < 0 or pos[1] >= len(map[0]):
        return None

    x, y = pos
    return map[x][y]


def move(pos, direction):
    x, y = pos
    dx, dy = movement[direction]
    return (x + dx, y + dy)


def printMap(map, playerPos, playerDir):
    for x in range(len(map)):
        for y in range(len(map[0])):
            if (x, y) == playerPos:
                print(playerReverse[playerDir], end="")
            else:
                print(map[x][y], end="")
        print()
    print()


def copyMap(map):
    return [row[:] for row in map]


movement = {
    "left": (0, -1),
    "right": (0, 1),
    "up": (-1, 0),
    "down": (1, 0),
    "leftUp": (-1, -1),
    "leftDown": (1, -1),
    "rightUp": (-1, 1),
    "rightDown": (1, 1),
}

# 90 rotation right
dirOrder = {
    "up": "right",
    "right": "down",
    "down": "left",
    "left": "up",
}
player = {"^": "up", "v": "down", "<": "left", ">": "right"}
playerReverse = {v: k for k, v in player.items()}

Empty = "."
Occupied = "#"
Visited = "X"
Obstructed = "0"
Walls = [Occupied, Obstructed]
initialPos = (0, 0)
initialDir = ""

# find initial player position and direction
for x in range(len(map)):
    for y in range(len(map[0])):
        val = getVal((x, y), map)

        if val in player:
            initialPos = (x, y)
            initialDir = player[val]


map[initialPos[0]][initialPos[1]] = Empty


def evaluate(map, startingPos, startingDir):
    mapCopy = copyMap(map)
    visitedPos = [startingPos]
    pos = startingPos
    dir = startingDir
    isLoop = False
    # for each position xy as key concatenated with direction as array of values
    visitedMapWithDirections = {}

    while True:
        key = f"{pos[0]},{pos[1]}"

        if not key in visitedMapWithDirections:
            visitedMapWithDirections[key] = []

        if dir in visitedMapWithDirections[key]:
            isLoop = True
            break

        visitedMapWithDirections[key].append(dir)

        mapCopy[pos[0]][pos[1]] = Visited
        # printMap(map, pos, dir)

        nextPos = move(pos, dir)
        val = getVal(nextPos, mapCopy)

        if not val:
            break

        if val in Walls:
            dir = dirOrder[dir]
            continue

        pos = nextPos
        if val == Empty:
            visitedPos.append(pos)

    if isLoop:
        return None

    return visitedPos


# first part
firstVisited = evaluate(map, initialPos, initialDir)
# print(len(firstVisited))

# # second part
res_second = 0
for obstructionPos in firstVisited:
    x,y = obstructionPos
    val = getVal(obstructionPos, map)

    if val == Empty:
        mapCopy = [row[:] for row in map]
        mapCopy[x][y] = Obstructed

        result = evaluate(mapCopy, initialPos, initialDir)

        if result is None:
            res_second += 1
            continue

print(res_second)
