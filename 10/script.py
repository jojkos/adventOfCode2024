class Map:
    movement = {
        "left": (0, -1),
        "right": (0, 1),
        "up": (-1, 0),
        "down": (1, 0),
    }

    dirs = {
        "left": "<",
        "right": ">",
        "up": "^",
        "down": "v",
    }

    def __init__(self, fileName):
        with open("input.txt", "r") as file:
            input = file.readlines()

        # remove newlines and parse each value as int
        self.map = [[int(char) for char in line.strip()] for line in input]

    def print(self):
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

    # path is from 0 to 9
    def findPaths(self, startingPos, foundEndings = []):
        x, y = startingPos
        val = self.map[x][y]        

        if val == 9:
            ending = str(x)+"-"+str(y)
            
            if ending not in foundEndings:
                foundEndings.append(ending)
            return 1

        allFound = 0

        for direction in self.movement:
            dx, dy = self.movement[direction]
            newX, newY = x + dx, y + dy

            if not self.isInsideMapBounds((newX, newY)):
                continue

            newVal = self.map[newX][newY]

            if val + 1 != newVal:
                continue

            allFound += self.findPaths((newX, newY), foundEndings)

        return allFound

    def solve(self):
        foundUnique = 0
        foundAll = 0

        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                if self.map[x][y] == 0:
                    foundEndings = []
                    foundAll += self.findPaths((x, y), foundEndings)
                    
                    foundUnique += len(foundEndings)
                    # print(x,y,foundEndings)

        print(foundUnique)
        print(foundAll)


map = Map("input.txt")

map.solve()
