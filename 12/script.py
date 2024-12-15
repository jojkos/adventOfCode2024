class Map:
    movement = {
        "left": (0, -1),
        "right": (0, 1),
        "up": (-1, 0),
        "down": (1, 0),
    }

    opposites = {
        "left": "right",
        "right": "left",
        "up": "down",
        "down": "up",
    }

    # neighbors = {
    #     "left": ["up", "down"],
    #     "right": ["up", "down"],
    #     "up": ["left", "right"],
    #     "down": ["left", "right"],
    # }

    # vertexCombination = [
    #     ["up", "left"], ["up", "right"], ["down", "left"], ["down", "right"],
    #     ["up", "left", "down" ], ["up", "right", "down" ], ["up", "left", "right" ], ["left", "down", "right" ]
    # ]

    diagonals = {
        "up-left": (-1, -1),
        "up-right": (-1, 1),
        "down-left": (1, -1),
        "down-right": (1, 1),
    }

    def __init__(
        self,
    ):
        with open("input.txt", "r") as file:
            input = file.readlines()

        # remove newlines
        self.map = [line.strip() for line in input]

    def print(self):
        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                print(self.map[x][y], end="")
            print()
        print()

    def isInsideMapBounds(self, pos):
        (x, y) = pos
        return x >= 0 and x < len(self.map) and y >= 0 and y < len(self.map[0])

    def getPerimeter(self, pos):
        x, y = pos
        perimeter = 0
        oppositeOnly = False
        firstFound = False

        for dir in self.movement:
            dx, dy = self.movement[dir]
            newX, newY = x + dx, y + dy

            if (
                not self.isInsideMapBounds((newX, newY))
                or self.map[newX][newY] != self.map[x][y]
            ):
                perimeter += 1

                if not firstFound:
                    firstFound = dir
                else:
                    opposite = self.opposites[firstFound]

                    if dir == opposite:
                        oppositeOnly = True

        return {
            "perimeter": perimeter,
            "opposites": oppositeOnly,
        }
    
    def posHasNeighbor(self, pos,dt):
        x, y = pos
        val = self.map[x][y]
        dx, dy = dt
        newX, newY = x + dx, y + dy

        if not self.isInsideMapBounds((newX, newY)):
            return False

        return self.map[newX][newY] == val

    def findRegions(self):
        visited = {}
        regions = []

        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                key = f"{x},{y}"

                if key in visited:
                    continue

                stack = [(x, y)]
                area = 0
                perimeter = 0
                vertices = 0

                visited[key] = True

                while len(stack) > 0:
                    currentX, currentY = stack.pop()
                    currentVal = self.map[currentX][currentY]

                    area += 1
                    currentPerimeter = self.getPerimeter((currentX, currentY))
                    perimeter += currentPerimeter["perimeter"]
                    currentVertices = 0

                    if currentPerimeter["perimeter"] == 4:
                        currentVertices = 4
                    elif currentPerimeter["perimeter"] == 2:
                        if not currentPerimeter["opposites"]:
                            currentVertices = 1
                    elif currentPerimeter["perimeter"] > 1:
                        newVertices = currentPerimeter["perimeter"] - 1
                        currentVertices = newVertices

                    found = 0

                    if self.posHasNeighbor((currentX, currentY), self.movement["up"]) and self.posHasNeighbor((currentX, currentY), self.movement["left"]):
                        if not self.posHasNeighbor((currentX, currentY), self.diagonals["up-left"]):
                            found += 1
                    if self.posHasNeighbor((currentX, currentY), self.movement["up"]) and self.posHasNeighbor((currentX, currentY), self.movement["right"]):
                        if not self.posHasNeighbor((currentX, currentY), self.diagonals["up-right"]):
                            found += 1
                    if self.posHasNeighbor((currentX, currentY), self.movement["down"]) and self.posHasNeighbor((currentX, currentY), self.movement["left"]):
                        if not self.posHasNeighbor((currentX, currentY), self.diagonals["down-left"]):
                            found += 1
                    if self.posHasNeighbor((currentX, currentY), self.movement["down"]) and self.posHasNeighbor((currentX, currentY), self.movement["right"]):
                        if not self.posHasNeighbor((currentX, currentY), self.diagonals["down-right"]):
                            found += 1

                    currentVertices += found

                    vertices += currentVertices

                    for dir in self.movement:
                        dx, dy = self.movement[dir]
                        newX, newY = currentX + dx, currentY + dy
                        newKey = f"{newX},{newY}"

                        if (
                            not self.isInsideMapBounds((newX, newY))
                            or newKey in visited
                        ):
                            continue

                        newVal = self.map[newX][newY]

                        if newVal != currentVal:
                            continue

                        stack.append((newX, newY))
                        visited[newKey] = True

                regions.append(
                    {
                        "area": area,
                        "perimeter": perimeter,
                        "vertices": vertices,
                        "val": currentVal,
                    }
                )

        # print(regions)

        return regions


field = Map()

regions = field.findRegions()

price = 0
price2 = 0

for region in regions:
    price += region["area"] * region["perimeter"]
    price2 += region["area"] * region["vertices"]

print(price)
print(price2)
