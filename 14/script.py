from PIL import Image

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
            valAtPos = self.map[posX][posY]

            if valAtPos == self.Empty:
                self.map[posX][posY] = []

            self.map[posX][posY].append((velX, velY))

    def print(self, ignoreMiddle=False):
        map = self.map

        xMid = self.height // 2
        yMid = self.width // 2

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

    def putpixel(self, img, x, y, color):
        img.putpixel((x, y), color)


    def printImg(self, t):        
        img = Image.new("RGB", (self.width, self.height), (255, 255, 255))

        map = self.map

        for x in range(len(map)):
            for y in range(len(map[0])):
                if map[x][y] == self.Empty:
                    self.putpixel(img, y, x, (255, 255, 255))
                else:
                    self.putpixel(img, y, x, (255, 0, 0))

        img.save(f"out/{t}.png")
        

    def isInsideMapBounds(self, pos, map):
        (x, y) = pos
        return x >= 0 and x < len(map) and y >= 0 and y < len(map[0])

    def move(self, robots, count):
        map = self.map
        newMap = [[self.Empty for y in range(len(map[0]))] for x in range(len(map))]
        newRobots = []

        for robot in robots:
            posX, posY = robot["pos"]
            velX, velY = robot["vel"]
            newPosX, newPosY = (posX + (velX * count), posY + (velY * count))

            newPosX = newPosX % len(map)
            newPosY = newPosY % len(map[0])

            if newMap[newPosX][newPosY] == self.Empty:
                newMap[newPosX][newPosY] = []

            newMap[newPosX][newPosY].append(vel)
            newRobots.append({"pos": (newPosX, newPosY), "vel": (velX, velY)})

        self.map = newMap

        return newRobots

    def countRobotsInQuadrants(self):
        xMid = self.height // 2
        yMid = self.width // 2
        quadrants = [0, 0, 0, 0]

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

# width = 11
# height = 7
width = 101
height = 103
robots = []

for line in input:
    pos, vel = line.split(" ")
    pos = pos.split("=")[1]
    posY, posX = [int(i) for i in pos.split(",")]
    vel = vel.split("=")[1]
    velY, velX = [int(i) for i in vel.split(",")]

    robots.append({"pos": (posX, posY), "vel": (velX, velY)})

map = Map(width, height, robots)

t = 10000

# map.print(True)


for i in range(t):
    robots = map.move(robots, 1)
    map.printImg(i+1)

# map.print() 
# map.printImg(1)
# map.countRobotsInQuadrants()
