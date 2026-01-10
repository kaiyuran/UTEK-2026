import math
def makeAdjList(adjList):
    adjList = adjList.split("\n")
    # print(adjList)
    adjList = [line.strip(",").split(": ") for line in adjList]
    for line in adjList:
        line[0] = int(line[0])
        line[1] = [int(i) for i in line[1][1:-1].split(", ")]
    return dict(adjList)

def makeCoods(botCoords):
    botCoords = botCoords.split("\n")
    botCoords = [line.strip().split(",") for line in botCoords]
    for line in botCoords:
        line[0] = int(line[0])
        line[1] = int(line[1])
    return botCoords

def nodeToCoord(node, gridDimensions):
    n, m = gridDimensions
    y = math.ceil(node / m) - 1
    x = (node - m * y) - 1
    return (x, y)
