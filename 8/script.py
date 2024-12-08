with open("input.txt", "r") as file:
    data = file.readlines()

# remove \n from each line and split each line into a list of characters
map = [list(line.strip()) for line in data]


def printMap(map):
    for x in range(len(map)):
        for y in range(len(map[0])):
            print(map[x][y], end="")
        print()
    print()


def isInsideMapBounds(map, pos):
    (x, y) = pos
    return x >= 0 and x < len(map) and y >= 0 and y < len(map[0])


def copyMap(map):
    return [row[:] for row in map]


def getDistance(pos1, pos2):
    (x1, y1) = pos1
    (x2, y2) = pos2
    return abs(x1 - x2) + abs(y1 - y2)


def isAntinode(posAntenna1, posAntenna2, pos):
    distance1 = getDistance(posAntenna1, pos)
    distance2 = getDistance(posAntenna2, pos)

    return abs(distance1 - distance2) == min(distance1, distance2)


Empty = "."
Antinode = "#"
antennas = {}

for x in range(len(map)):
    for y in range(len(map[x])):
        val = map[x][y]

        if val != Empty:
            if val not in antennas:
                antennas[val] = []
            antennas[val].append((x, y))


def solve_one():
    antinodes = {}
    res = 0
    mapCopy = copyMap(map)

    for type in antennas:
        # for each two antennas of same type
        for i in range(len(antennas[type])):
            for j in range(i + 1, len(antennas[type])):
                antenna1 = antennas[type][i]
                antenna2 = antennas[type][j]
                dx = antenna2[0] - antenna1[0]
                dy = antenna2[1] - antenna1[1]

                # print(dx, dy)

                possibleAntinodes = [
                    (antenna1[0] - dx, antenna1[1] - dy),
                    (antenna2[0] + dx, antenna2[1] + dy),
                ]

                for possibleAntinode in possibleAntinodes:
                    if isInsideMapBounds(mapCopy, possibleAntinode):
                        mapCopy[possibleAntinode[0]][possibleAntinode[1]] = Antinode
                        key = (
                            "x"
                            + str(possibleAntinode[0])
                            + "y"
                            + str(possibleAntinode[1])
                        )

                        if key not in antinodes:
                            antinodes[key] = True
                            res += 1

        # print(type)
        # printMap(mapCopy)

    # printMap(mapCopy)
    # print(antinodes)
    print(res)


def moveUntilOutOfBounds(map, pos, dx, dy):
    visitedPos = []
    (x, y) = pos

    while isInsideMapBounds(map, (x + dx, y + dy)):
        x += dx
        y += dy
        visitedPos.append((x, y))

    return visitedPos


def solve_two():
    antinodes = {}
    res = 0
    mapCopy = copyMap(map)

    for type in antennas:
        # for each two antennas of same type
        for i in range(len(antennas[type])):
            for j in range(i + 1, len(antennas[type])):
                antenna1 = antennas[type][i]
                antenna2 = antennas[type][j]
                dx = antenna2[0] - antenna1[0]
                dy = antenna2[1] - antenna1[1]

                # create antinodes array from the results of moveUntilOutOfBounds
                possibleAntinodes = []
                possibleAntinodes += moveUntilOutOfBounds(mapCopy, antenna1, dx, dy)
                possibleAntinodes += moveUntilOutOfBounds(mapCopy, antenna2, -dx, -dy)

                for pos in possibleAntinodes:
                    key = "x" + str(pos[0]) + "y" + str(pos[1])
                    if key not in antinodes:
                        res += 1
                        antinodes[key] = True
                        mapCopy[pos[0]][pos[1]] = Antinode

        # print(type)
        # printMap(mapCopy)

    # printMap(mapCopy)
    print(res)


solve_one()
solve_two()
