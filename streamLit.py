import streamlit as st
from parsingFuncs import makeAdjList, makeCoods, nodeToCoord
from calculations import Calculations

adjList = st.text_area("adjList", 
"""1: [2, 3]
2: [1, 4, 5]
3: [1, 6]
4: [2, 7]
5: [2, 8]
6: [3, 9]
7: [4]
8: [5]
9: [6]""")
adjList = makeAdjList(adjList)

dimensions = st.text_input("dimensions (nxm)", "10,10")

st.write("The current adjLists is", str(adjList))


botCoords = st.text_area("droid coordinates in order of importance", 
"""1,2
2,3
3,4
5,6
6,7""")
botCoords = makeCoods(botCoords)
# print(botCoords)
st.write("The current adjList is", str(botCoords))

drones = []
for i, coord in enumerate(botCoords):
    drones.append({"id": i + 1, "start": coord[0], "end": coord[1]})

calc = Calculations(adjList, paths_needed=3, velocity=1.0)
schedule = calc.schedule(drones)


sendtoplot = []
print(schedule)
for droid in schedule:
    sendtoplot.append(schedule[droid][0])
    # print(type(schedule[droid][0]))


print("sendtoplot:", sendtoplot)
# for line in sendtoplot:
#     # print(line)
#     for point in line:
#         point = nodeToCoord(point, (int(dimensions.split(",")[0]), int(dimensions.split(",")[1])))

# print("sendtoplot", sendtoplot)




#TODO FINISH adding zoning
restrictedAdjList = st.text_area("Optional restricted zone adjList","")

usingRestricted = False
restrictedBotCoords = st.text_area("Optional restricted droid zone coordinates","")


if restrictedBotCoords != "" and restrictedAdjList != "":
    usingRestricted = True
    restrictedAdjList = makeAdjList(restrictedAdjList)
    restrictedBotCoords = makeCoods(restrictedBotCoords)

st.subheader(r"This is the path schedule in format {droid_id: ([route], start_time)...}")
st.write(str(schedule))