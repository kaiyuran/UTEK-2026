import turtle


#still working on it

def drawMap(dimensions, adjList, coordinates):

    def coordToPos



    screen = turtle.Screen()
    screen.setup(width=600, height=400)
    screen.bgcolor("white")
    pen = turtle.Turtle()
    pen.shape("circle")
    # pen.ht()
    pen.speed(0)



    #draw grid using dimensions nxm
    pen.pensize(1)
    pen.color("lightgrey")
    n, m = dimensions
    cellWidth = (screen.window_width()-20) / (n+1)
    cellHeight = (screen.window_height()-20) / (m+1)
    startX = (-screen.window_width() / 2) + cellWidth
    startY = (screen.window_height() / 2) - cellHeight
    for i in range(n + 1):
        pen.penup()
        pen.goto(startX + i * cellWidth, startY)
        pen.pendown()
        pen.goto(startX + i * cellWidth, startY - m * cellHeight)

    for j in range(m + 1):
        pen.penup()
        pen.goto(startX, startY - j * cellHeight)
        pen.pendown()
        pen.goto(startX + n * cellWidth, startY - j * cellHeight)
    pen.penup()

    # pen.goto(0,0)
    # pen.pensize(3)
    # pen.color("black")

    #draw paths using nodes in adjList


    screen.exitonclick()

drawMap((60, 40), {}, {})
