with open("input.txt", "r") as file:
    data = file.readlines()

movement = {
    "left": (0,-1),
    "right": (0,1),
    "up": (-1,0),
    "down": (1,0),
    "leftUp": (-1,-1),
    "leftDown": (1,-1),
    "rightUp": (-1,1),
    "rightDown": (1,1)
}

def getVal(pos):
    if pos[0] < 0 or pos[0] >= len(data):
        return None
    if pos[1] < 0 or pos[1] >= len(data[0]):
        return None

    x, y = pos
    return data[x][y]

def applyDirection(pos, direction):
    x, y = pos
    dx, dy = movement[direction]
    return (x+dx, y+dy)

def findWord(pos, target, direction):
    found = ""
    currentPos = pos
    
    while True:
        char = getVal(currentPos)
        if char is None:
            return False

        found += char

        if not target.startswith(found):            
            return False
        
        if found == target:
            return currentPos
        
        currentPos = applyDirection(currentPos, direction)
        

data = [line.strip() for line in data]

def solve_part_one():
    TARGET = "XMAS"
    result_one = 0

    for x in range(len(data)):
        for y in range(len(data[0])):
            for direction in movement:            
                pos = (x,y)
                
                if (findWord(pos, TARGET, direction)):
                    result_one += 1

    print(result_one)    


def solve_part_two():
    result_two = 0
    targets = ["MAS", "SAM"]
    dirs = ["rightDown"]

    for x in range(len(data)):
        for y in range(len(data[0])):            
            pos = (x, y)
            found = False

            for i in range(len(dirs)):
                for target in targets:
                    foundPos = findWord(pos, target, dirs[i])

                    if foundPos:      
                        # print(pos, target, dirs[i])
                        nextDir = "rightUp"
                        nextPos = (foundPos[0], foundPos[1] - 2)
                                            
                        for innerTarget in targets:                        
                            foundSecond = findWord(nextPos, innerTarget, nextDir)

                            if foundSecond:
                                # print("inner",nextPos, innerTarget, nextDir)
                                result_two += 1
                                break
                

    print(result_two)

solve_part_one()
solve_part_two()