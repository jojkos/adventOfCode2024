from itertools import combinations, permutations

def getAllCombinations(lst, N):
    return list(combinations(lst, N))

with open("input.txt", "r") as file:
    input = file.readlines()
    # remove newline characters and parse int
    input = [x.strip() for x in input]

nodes = {}

for line in input:
    n1, n2 = line.split("-")

    if n1 not in nodes:
        nodes[n1] = []
    if n2 not in nodes:
        nodes[n2] = []
    
    nodes[n1].append(n2)
    nodes[n2].append(n1)

def getGroups(groupSize):
    groups = []
    c = 0

    for node in nodes:
        possibleGroups = getAllCombinations([node] + nodes[node], groupSize)        
        print(c)
        for possibleGroup in possibleGroups:
            isGroup = True
            sortedPossibleGroup = sorted(possibleGroup)
            key = ",".join(sortedPossibleGroup)

            if key in groups:
                continue

            if (sortedPossibleGroup[0] == "aq") and sortedPossibleGroup[1]  == "cg" and sortedPossibleGroup[2] == "yn":
                print(sortedPossibleGroup)
            
            for i in range(len(sortedPossibleGroup)):
                for j in range(1, len((sortedPossibleGroup))):
                    n1 = sortedPossibleGroup[i]
                    n2 = sortedPossibleGroup[j]

                    if n1 == n2:
                        continue

                    if n2 not in nodes[n1] or n1 not in nodes[n2]:
                        isGroup = False
                        break
            if isGroup:
                groups.append(key)
        c += 1

    return groups

def findBiggestGroup():
    maxNodes = 0

    for node in nodes:
        childrenLen = len(nodes[node])
        
        if childrenLen > maxNodes:
            maxNodes = childrenLen
            
    groups = getGroups(maxNodes)
    print("res2", groups)

# groups = getGroups(3)
# # print(len(groups))
# # print(groups)
# sum = 0

# for group in groups:
#     nodes = group.split(",")
#     tFound = False

#     for node in nodes:
#         if node.startswith("t"):
#             tFound = True
#             break
#     if tFound:
#         sum += 1
# print("res1", sum)

findBiggestGroup()