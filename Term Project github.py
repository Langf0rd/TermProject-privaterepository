###########################################
# Vinay Mitta, vmitta, Section J
###########################################
#
# events-example0.py
# Barebones timer, mouse, and keyboard events taken from 
# https://www.cs.cmu.edu/~112/notes/hw5.html
# change
from tkinter import *
import math

####################################
# customize these functions
####################################

def init(data):
    data.centerx = data.width/2
    data.centery = data.height/2
    initMap(data)
    initPlayer(data)

# 
def initMap(data):
    data.mapLength = 10000
    data.mapWidth = 10000
    data.mapHeight = 5000

def initPlayer(data):
    data.playerPosition = [5000, -1000, 2000, 0, 0]

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    if event.keysym == "w": # Temporary for testing, need to align with angle
        data.playerPosition[1] += 100
    if event.keysym == "s":
        data.playerPosition[1] -= 100
    if event.keysym == "d":
        data.playerPosition[0] += 100
    if event.keysym == "a":
        data.playerPosition[0] -= 100
    if event.keysym == "Up":
        data.playerPosition[4] += 1
    if event.keysym == "Down":
        data.playerPosition[4] -= 1
    if event.keysym == "Left":
        data.playerPosition[3] += 1
    if event.keysym == "Right":
        data.playerPosition[3] -= 1

def timerFired(data):
    pass

def redrawAll(canvas, data):
    drawCrosshairs(canvas, data)
    drawMapFloor(canvas, data)
    drawMapCiel(canvas, data)

def drawCrosshairs(canvas, data):
    canvas.create_rectangle(data.centerx - 30, data.centery - 30,
                            data.centerx + 30, data.centery + 30,
                            dash = (3,5))

def getBend(offset, distance, point, data):
    #(offset[1]/(((distance**2) - ((data.playerPosition[2] - point[2])**2))**0.5)/400)
    return ((offset[0]/(distance/400)), (offset[1]/(distance/400)))

def drawMapCiel(canvas, data): #All hardcoded for testing
    mapFloorCoords = ((0,0,4000),(0,10000,4000),(10000,10000,4000),(10000,0,4000))
    canvas.create_polygon(data.centerx + getBend((getOffset(mapFloorCoords[0], data.playerPosition)), getDistance(mapFloorCoords[0], data.playerPosition), mapFloorCoords[0], data)[0], 
                            data.centery + getBend((getOffset(mapFloorCoords[0], data.playerPosition)), getDistance(mapFloorCoords[0], data.playerPosition), mapFloorCoords[0], data)[1],
                            data.centerx + getBend((getOffset(mapFloorCoords[1], data.playerPosition)), getDistance(mapFloorCoords[1], data.playerPosition), mapFloorCoords[1], data)[0],
                            data.centery + getBend((getOffset(mapFloorCoords[1], data.playerPosition)), getDistance(mapFloorCoords[1], data.playerPosition), mapFloorCoords[1], data)[1],
                            data.centerx + getBend((getOffset(mapFloorCoords[2], data.playerPosition)), getDistance(mapFloorCoords[2], data.playerPosition), mapFloorCoords[2], data)[0],
                            data.centery + getBend((getOffset(mapFloorCoords[2], data.playerPosition)), getDistance(mapFloorCoords[2], data.playerPosition), mapFloorCoords[2], data)[1],
                            data.centerx + getBend((getOffset(mapFloorCoords[3], data.playerPosition)), getDistance(mapFloorCoords[3], data.playerPosition), mapFloorCoords[3], data)[0],
                            data.centery + getBend((getOffset(mapFloorCoords[3], data.playerPosition)), getDistance(mapFloorCoords[3], data.playerPosition), mapFloorCoords[3], data)[1],
                            fill = "light grey", outline = "black")
    # need to get offset, and then shift that offset for distance

def drawMapFloor(canvas, data): #All hardcoded for testing
    mapFloorCoords = ((0,0,0),(0,10000,0),(10000,10000,0),(10000,0,0))
    canvas.create_polygon(data.centerx + getBend((getOffset(mapFloorCoords[0], data.playerPosition)), getDistance(mapFloorCoords[0], data.playerPosition), mapFloorCoords[0], data)[0], 
                            data.centery + getBend((getOffset(mapFloorCoords[0], data.playerPosition)), getDistance(mapFloorCoords[0], data.playerPosition), mapFloorCoords[0], data)[1],
                            data.centerx + getBend((getOffset(mapFloorCoords[1], data.playerPosition)), getDistance(mapFloorCoords[1], data.playerPosition), mapFloorCoords[1], data)[0],
                            data.centery + getBend((getOffset(mapFloorCoords[1], data.playerPosition)), getDistance(mapFloorCoords[1], data.playerPosition), mapFloorCoords[1], data)[1],
                            data.centerx + getBend((getOffset(mapFloorCoords[2], data.playerPosition)), getDistance(mapFloorCoords[2], data.playerPosition), mapFloorCoords[2], data)[0],
                            data.centery + getBend((getOffset(mapFloorCoords[2], data.playerPosition)), getDistance(mapFloorCoords[2], data.playerPosition), mapFloorCoords[2], data)[1],
                            data.centerx + getBend((getOffset(mapFloorCoords[3], data.playerPosition)), getDistance(mapFloorCoords[3], data.playerPosition), mapFloorCoords[3], data)[0],
                            data.centery + getBend((getOffset(mapFloorCoords[3], data.playerPosition)), getDistance(mapFloorCoords[3], data.playerPosition), mapFloorCoords[3], data)[1],
                            fill = "light grey", outline = "black")
    # need to get offset, and then shift that offset for distance

def getDistance(a, b):
    temp1 = ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5
    temp2 = (temp1**2+(a[2]-b[2])**2)**0.5
    return temp2

def getOffset(point, player):
    dist = getDistance(player, point)
    z = (player[2] - point[2])
    alpha = player[4]
    vertOff = ((math.sin(math.radians(90-alpha))) * 
                (z - dist*math.tan(math.radians(alpha))))
    x = (player[0] - point[0])
    y = (player[1] - point[1])
    theta = player[3]
    horOff = ((math.sin(math.radians(90-theta))) * 
                (x-y*math.tan(math.radians(theta))))
    return (horOff, vertOff)


class cube(object):
    def __init__(self, x1, y1, z1, length):
        self.x1 = x1
        self.x2 = x1 + length

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(600, 600)