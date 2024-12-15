class Map:
    movement = {
        "left": (0, -1),
        "right": (0, 1),
        "up": (-1, 0),
        "down": (1, 0),
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

        for dir in self.movement:
            dx, dy = self.movement[dir]
            newX, newY = x + dx, y + dy

            if (
                not self.isInsideMapBounds((newX, newY))
                or self.map[newX][newY] != self.map[x][y]
            ):
                perimeter += 1

        return perimeter

    def findRegions(self):
        visited = []
        regions = []

        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                key = f"{x},{y}"

                if key in visited:
                    continue

                stack = [(x, y)]
                area = 0
                perimeter = 0

                visited.append(key)

                while len(stack) > 0:
                    currentX, currentY = stack.pop()
                    currentKey = f"{currentX},{currentY}"
                    currentVal = self.map[currentX][currentY]

                    area += 1
                    perimeter += self.getPerimeter((currentX, currentY))

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
                        visited.append(newKey)

                regions.append(
                    {"area": area, "perimeter": perimeter, "val": currentVal}
                )

        print(regions)

        return regions


field = Map()

regions = field.findRegions()

price = 0

for region in regions:
    price += region["area"] * region["perimeter"]

print(price)
