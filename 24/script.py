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
    while len(operations) > 0:
        op = operations.pop(0)
        firstWire, secondWire, operator, resultWire = op

        if not firstWire in wires or not secondWire in wires:
            operations.append(op)
            continue

        if operator == "AND":
            res = wires[firstWire] & wires[secondWire]
        elif operator == "OR":
            res = wires[firstWire] | wires[secondWire]
        elif operator == "XOR":
            res = wires[firstWire] ^ wires[secondWire]

        wires[resultWire] = res


    results  = []

    for wire in wires:
        if wire.startswith("z"):
            results.append([wire, wires[wire]])
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
# res = runWires(wires)
# print("res:", res, "expected", expectedResultDecimal)

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


# # Extract node positions
# x_nodes = [pos[node][0] for node in G.nodes()]
# y_nodes = [pos[node][1] for node in G.nodes()]

# # Extract edges for visualization
# edges = G.edges()
# x_edges = []
# y_edges = []
# for edge in edges:
#     x0, y0 = pos[edge[0]]
#     x1, y1 = pos[edge[1]]
#     x_edges.append(x0)
#     x_edges.append(x1)
#     y_edges.append(y0)
#     y_edges.append(y1)

# # Create Plotly figure
# fig = go.Figure()

# # Add edges as lines
# fig.add_trace(go.Scatter(x=x_edges, y=y_edges, mode='lines', line=dict(width=0.5, color='gray')))

# # Add nodes as points
# fig.add_trace(go.Scatter(x=x_nodes, y=y_nodes, mode='markers+text', text=[f'Node {i}' for i in G.nodes()],
#                          marker=dict(size=15, color='lightblue', line=dict(width=1, color='black')),
#                          textposition="bottom center"))

# # Set layout for better interactivity
# fig.update_layout(title="Interactive Graph", showlegend=False, hovermode='closest',
#                   xaxis=dict(showgrid=False, zeroline=False),
#                   yaxis=dict(showgrid=False, zeroline=False),
#                   plot_bgcolor='white')

# # Show the plot
# fig.show()