
class Map:
    movement = {
        "left": (0, -1),
        "right": (0, 1),
        "up": (-1, 0),
        "down": (1, 0),
    }

    Empty = "."

    def __init__(self, width, height, robots):
        self.width = width
        self.height = height
        self.map = [[self.Empty for y in range(width)] for x in range(height)]
        
        for robot in robots:
            posX, posY = robot["pos"]
            velX, velY = robot["vel"]
            try:
                valAtPos = self.map[posX][posY]        
            except IndexError:
                print("IndexError at", posX, posY)
                exit()

            if valAtPos == self.Empty:
                self.map[posX][posY] = []
            
            self.map[posX][posY].append((velX, velY))

        
    def print(self, ignoreMiddle = False):
        map = self.map

        xMid = round(self.height / 2) - 1
        yMid = round(self.width / 2) - 1

        for x in range(len(map)):
            for y in range(len(map[0])):
                if ignoreMiddle and (x == xMid or y == yMid):
                    print(" ", end="")
                    continue

                if map[x][y] == self.Empty:
                    print(".", end="")
                else:
                    print(len(map[x][y]), end="")
            print()
        print()

    def isInsideMapBounds(self, pos, map):
        (x, y) = pos
        return x >= 0 and x < len(map) and y >= 0 and y < len(map[0])
    
    def move(self):
        map = self.map
        newMap = [[self.Empty for y in range(len(map[0]))] for x in range(len(map))]

        for x in range(len(map)):
            for y in range(len(map[0])):
                if map[x][y] != self.Empty:
                    for vel in map[x][y]:
                        (velX, velY) = vel
                        newPosX, newPosY = (x + velX, y + velY)

                        newPosX = newPosX % len(map)
                        newPosY = newPosY % len(map[0])

                        if newMap[newPosX][newPosY] == self.Empty:
                            newMap[newPosX][newPosY] = []

                        newMap[newPosX][newPosY].append(vel)

        self.map = newMap

    def countRobotsInQuadrants(self):
        xMid = round(self.height / 2) - 1
        yMid = round(self.width / 2) - 1

        quadrants = [0,0,0,0]

        for x in range(len(self.map)):
            for y in range(len(self.map[0])):
                if x == xMid or y == yMid:
                    continue

                if x < xMid and y < yMid:
                    quadrantIndex = 0
                elif x < xMid and y > yMid:
                    quadrantIndex = 1
                elif x > xMid and y < yMid:
                    quadrantIndex = 2
                elif x > xMid and y > yMid:
                    quadrantIndex = 3

                if self.map[x][y] != self.Empty:
                    quadrants[quadrantIndex] += len(self.map[x][y])
                
        res = quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]

        print(quadrants)
        print(res)


with open("input.txt", "r") as file:
        # read all lines, remove new line character
    input = [line.strip() for line in file.readlines()]

width = 11
height = 7
# width = 101
# height = 103
robots = []

for line in input:
    pos, vel = line.split(" ")
    pos = pos.split("=")[1]
    posY, posX = [int(i) for i in pos.split(",")]
    vel = vel.split("=")[1]
    velY, velX = [int(i) for i in vel.split(",")]

    robots.append({
        "pos": (posX, posY),
        "vel": (velX, velY)
    })

map = Map(width, height, robots)

t = 100

map.print()
for i in range(t):
    map.move()
    # map.print()

map.print()
map.countRobotsInQuadrants()