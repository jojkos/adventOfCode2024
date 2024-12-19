with open("input.txt", "r") as file:
    input = file.readlines()
    # remove new line
    input = [x.strip() for x in input]

patterns = input[0].split(",")
# strip each pattern
patterns = [x.strip() for x in patterns]
designs = input[2:]
cache={}

def matchDesign(design, i=0):
    global cache

    if i == len(design):
        return 1

    remainingDesign = design[i:]

    if cache.get(remainingDesign) is not None:
        val = cache[remainingDesign]

        return val
    
    matchFound = False

    for pattern in patterns:
        if len(remainingDesign) >= len(pattern) and remainingDesign.startswith(pattern):
            res = matchDesign(design, i + len(pattern))

            if res:
                matchFound = True
                # print("found:", remainingDesign, pattern , res)

                if not remainingDesign in cache:
                    cache[remainingDesign] = 0
                cache[remainingDesign] += res

    if not matchFound:
        cache[remainingDesign] = False

    return cache[remainingDesign]


count = 0

i = 0
for design in designs:
    i += 1
    print(i)
    res = matchDesign(design)

    if res:
        count += 1

# print("res:", count)

sum = 0
for design in designs:
    # print(design, cache[design])
    sum += cache[design]

print(sum)