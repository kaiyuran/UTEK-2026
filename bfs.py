import time

def bfs(AdjDict, startNode, endNode, pathsNeeded):
    currPaths = [[startNode]] #check later
    visitedNodes = [startNode]
    foundPath = False
    finalPaths = []
    while not foundPath:
        newPaths = []
        for path in currPaths:
            for node in AdjDict[path[-1]]:
                if node == endNode:
                    finalPaths.append(path + [node])

                # elif not node in visitedNodes:
                elif not node in path:
                    visitedNodes.append(node)
                    newPaths.append(path + [node])

        if len(finalPaths) > (pathsNeeded-1) or len(newPaths) == 0:
            break

        currPaths = newPaths
        # time.sleep(.5)

    if len(finalPaths) > pathsNeeded:
        finalPaths = finalPaths[:pathsNeeded]

    return(finalPaths)