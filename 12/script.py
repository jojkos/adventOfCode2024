class Map:
    movement = {
        "left": (0, -1),
        "right": (0, 1),
        "up": (-1, 0),
        "down": (1, 0),
    }

    def __init__(self, ):
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

            if not self.isInsideMapBounds((newX, newY)) or self.map[newX][newY] != self.map[x][y]:
                perimeter += 1

        return perimeter

    def findRegions(self):
        regions = {}
        
        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                val = self.map[x][y]

                if val not in regions:
                    regions[val] = {"area": 0, "perimeter": 0}
                
                regions[val]["area"] += 1
                regions[val]["perimeter"] += self.getPerimeter((x, y))

        print(regions)

        return regions


field = Map()

regions = field.findRegions()

price = 0

for region in regions:
    price += regions[region]["area"] * regions[region]["perimeter"]

print(price)