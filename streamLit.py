import streamlit as st
from parsingFuncs import makeAdjList, makeCoods, nodeToCoord


adjList = st.text_area("adjList", 
"""1: [2, 3, 4, 5, 6],
2: [1, 3, 4, 5, 7],
3: [1, 2, 4, 6, 8],
4: [1, 2, 3, 5, 7],
5: [1, 2, 4, 6],
6: [1, 3, 5, 7],
7: [2, 4, 6, 8],
8: [3, 7]""")
adjList = makeAdjList(adjList)



st.write("The current adjLists is", str(adjList))


botCoords = st.text_area("droid coordinates in order of importance", 
"""1,2
2,3
3,4
5,6
6,7""")
botCoords = makeCoods(botCoords)
print(botCoords)
st.write("The current adjList is", str(botCoords))



restrictedAdjList = st.text_area("Optional restricted adjList","")

usingRestricted = False
restrictedBotCoords = st.text_area("Optional restricted droid coordinates","")


if restrictedBotCoords != "" and restrictedAdjList != "":
    usingRestricted = True
    restrictedAdjList = makeAdjList(restrictedAdjList)
    restrictedBotCoords = makeCoods(restrictedBotCoords)


