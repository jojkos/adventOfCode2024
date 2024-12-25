import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go

with open("input.txt", "r") as file:
    input = file.readlines()
    # remove newline characters and parse int
    input = [x.strip() for x in input]

parsingFirstPart = True

wires = {}
operations = []

for line in input:
    if line == "":
        parsingFirstPart = False
        continue

    if parsingFirstPart:
        # parsing first part
        wire, value = line.split(" ")
        wire = wire.replace(":", "").strip()
        value = int(value.strip())
        wires[wire] = value
    else:
        values = line.split(" ")
        firstWire = values[0]
        secondWire = values[2]
        operator = values[1]
        resultWire = values[-1]

        operations.append((firstWire, secondWire, operator, resultWire))

def runWires(wires):
    wiresClone = wires.copy()
    operationsClone = operations.copy()

    while len(operationsClone) > 0:
        op = operationsClone.pop(0)
        firstWire, secondWire, operator, resultWire = op

        if not firstWire in wiresClone or not secondWire in wiresClone:
            operationsClone.append(op)
            continue

        if operator == "AND":
            res = wiresClone[firstWire] & wiresClone[secondWire]
        elif operator == "OR":
            res = wiresClone[firstWire] | wiresClone[secondWire]
        elif operator == "XOR":
            res = wiresClone[firstWire] ^ wiresClone[secondWire]
        
        # if resultWire.startswith("z"):
        #     if operator != "XOR":
        #         print(operator, firstWire, secondWire, resultWire)

        wiresClone[resultWire] = res


    results  = []
    
    for wire in wiresClone:
        if wire.startswith("z"):
            results.append([wire, wiresClone[wire]])
    # sort results by wire name
    results.sort(key=lambda x: x[0])
    output = ""

    for result in results:
        output = str(result[1]) + output

    return output

# print("part one:", int(runWires(wires), 2))


# part two
xWires = []
yWires = []
for wire in wires:
    if wire.startswith("x"):
        xWires.append([wire, wires[wire]])
    if wire.startswith("y"):
        yWires.append([wire, wires[wire]])
# sort wires by name
xWires.sort(key=lambda x: x[0])
yWires.sort(key=lambda x: x[0])
xInput = ""
yInput = ""

for wire in xWires:
    xInput = str(wire[1]) + xInput
for wire in yWires:
    yInput = str(wire[1]) + yInput

xDecimal = int(xInput, 2)
yDecimal = int(yInput, 2)

expectedResultDecimal = xDecimal + yDecimal
expectedResultBinary = bin(expectedResultDecimal)[2:]

# print(xInput, yInput, bin(xDecimal & yDecimal)[2:])



# try to all combinations of 4 output wires to get correct result
res = runWires(wires)
# print("res:", int(res, 2), "expected", expectedResultDecimal)
print("res:", res, "expected", expectedResultBinary)
print(res == expectedResultBinary)
print("length:", len(expectedResultBinary))

# go over each character of expectedResultBinary backwards
for i in range(len(expectedResultBinary) - 1, -1, -1):
    # print(i)
    if expectedResultBinary[i] != res[i]:
        print("different at index", i)
        

nodeIds = {}

for w in wires.keys():
    nodeIds[w] = True

edgesArray = []
edge_labels = {}

for op in operations:
    firstWire, secondWire, operator, resultWire = op
    edgesArray.append((firstWire, resultWire))
    edgesArray.append((secondWire, resultWire))
    
    if resultWire not in nodeIds:
        nodeIds[resultWire] = True

    edge_labels[(firstWire, resultWire)] = operator
    edge_labels[(secondWire, resultWire)] = operator

# Create a graph
G = nx.DiGraph()

G.add_nodes_from(nodeIds)
G.add_edges_from(edgesArray)

# Use spring layout for node positioning
pos = nx.kamada_kawai_layout(G)

# Draw the graph
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=1500, font_size=15, arrows=True)
# Draw edge labels
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_color='red')

# Show the plot
plt.show()
