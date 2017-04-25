###########################################
# Vinay Mitta, vmitta, Section J
###########################################

# events-example0.py
# Barebones timer, mouse, and keyboard events taken from 
# https://www.cs.cmu.edu/~112/notes/hw5.html

from tkinter import *
import math

####################################
# customize these functions
####################################

def init(data):
    data.cenX = data.width/2
    data.cenY = data.height/2
    initPlayer(data)
    data.mode = "map1"
    if data.mode == "map1":
        initMap1(data)


def initMap1(data):
    data.cube1 = cube(5000,5000,2000,300)
    data.cube2 = cube(1000,1000,1000,600)
    data.cube3 = cube(9000,2000,200,500)



def initPlayer(data):
    data.playerPos = [5000, -1000, 1500, 0, 0]

def mousePressed(event, data):
    # use event.x and event.y
    pass


def keyPressed(event, data):
    if event.keysym == "w":
        data.playerPos[1] += 100*math.cos(math.radians((data.playerPos[3])))
        data.playerPos[0] += 100*math.sin(math.radians((data.playerPos[3]))) # Need to change so its when pressed not single press
    if event.keysym == "s":
        data.playerPos[1] += 100*math.cos(math.radians((data.playerPos[3] + 180)))
        data.playerPos[0] += 100*math.sin(math.radians((data.playerPos[3] + 180)))
    if event.keysym == "d":
        data.playerPos[1] += 100*math.cos(math.radians((data.playerPos[3] + 270)))
        data.playerPos[0] += 100*math.sin(math.radians((data.playerPos[3] + 270)))
    if event.keysym == "a":
        data.playerPos[1] += 100*math.cos(math.radians((data.playerPos[3] + 90)))
        data.playerPos[0] += 100*math.sin(math.radians((data.playerPos[3] + 90)))
    if event.keysym == "Up":
        if data.playerPos[4] < 60:
            data.playerPos[4] += 1 # Need to change it to the mouse movement
    if event.keysym == "Down":
        if data.playerPos[4] > -60:
            data.playerPos[4] -= 1
    if event.keysym == "Left":
        data.playerPos[3] += 1
        if data.playerPos[3] == 90 or data.playerPos[3] == 270:
            data.playerPos[3] += 1
        print(data.playerPos[3])
    if event.keysym == "Right":
        data.playerPos[3] -= 1
        if data.playerPos[3] == 90 or data.playerPos[3] == 270:
            data.playerPos[3] -= 1

def timerFired(data):
    pass

def redrawAll(canvas, data):
    drawCrosshairs(canvas, data)
    drawMapFloor(canvas, data)
    drawMapCiel(canvas, data)
    data.cube1.draw(canvas, data)
    data.cube2.draw(canvas, data)
    data.cube3.draw(canvas, data)

def drawCrosshairs(canvas, data):
    canvas.create_rectangle(data.cenX - 30, data.cenY - 30,
                            data.cenX + 30, data.cenY + 30,
                            dash = (3,5))

def getBend(offset, distance, point, data):
    #(offset[1]/(distance/400))
    xBen = (offset[0]/(distance/1200))
    yBen = (offset[1]/((((distance**2) - ((data.playerPos[2] - point[2])**2))**0.5)/1200))
    x = (data.playerPos[0] - point[0])
    y = (data.playerPos[1] - point[1])
    #alpha = math.degrees(math.atan(x/y))
    #theta = data.playerPos[3]
    #if theta - alpha > 89:
    #    yBen = yBen*data.width
    return (xBen, yBen)

def drawMapCiel(canvas, data): #All hardcoded for testing
    mapFlr = ((0,0,4000),(0,10000,4000),(10000,10000,4000),(10000,0,4000))
    canvas.create_polygon(data.cenX + getBend((getOffset(mapFlr[0], data.playerPos)), getDistance(mapFlr[0], data.playerPos), mapFlr[0], data)[0], 
                            data.cenY + getBend((getOffset(mapFlr[0], data.playerPos)), getDistance(mapFlr[0], data.playerPos), mapFlr[0], data)[1],
                            data.cenX + getBend((getOffset(mapFlr[1], data.playerPos)), getDistance(mapFlr[1], data.playerPos), mapFlr[1], data)[0],
                            data.cenY + getBend((getOffset(mapFlr[1], data.playerPos)), getDistance(mapFlr[1], data.playerPos), mapFlr[1], data)[1],
                            data.cenX + getBend((getOffset(mapFlr[2], data.playerPos)), getDistance(mapFlr[2], data.playerPos), mapFlr[2], data)[0],
                            data.cenY + getBend((getOffset(mapFlr[2], data.playerPos)), getDistance(mapFlr[2], data.playerPos), mapFlr[2], data)[1],
                            data.cenX + getBend((getOffset(mapFlr[3], data.playerPos)), getDistance(mapFlr[3], data.playerPos), mapFlr[3], data)[0],
                            data.cenY + getBend((getOffset(mapFlr[3], data.playerPos)), getDistance(mapFlr[3], data.playerPos), mapFlr[3], data)[1],
                            fill = "light grey", outline = "black")
    # need to get offset, and then shift that offset for distance

def drawMapFloor(canvas, data): #All hardcoded for testing
    mapFlr = ((0,0,0),(0,10000,0),(10000,10000,0),(10000,0,0))
    canvas.create_polygon(data.cenX + getBend((getOffset(mapFlr[0], data.playerPos)), getDistance(mapFlr[0], data.playerPos), mapFlr[0], data)[0], 
                            data.cenY + getBend((getOffset(mapFlr[0], data.playerPos)), getDistance(mapFlr[0], data.playerPos), mapFlr[0], data)[1],
                            data.cenX + getBend((getOffset(mapFlr[1], data.playerPos)), getDistance(mapFlr[1], data.playerPos), mapFlr[1], data)[0],
                            data.cenY + getBend((getOffset(mapFlr[1], data.playerPos)), getDistance(mapFlr[1], data.playerPos), mapFlr[1], data)[1],
                            data.cenX + getBend((getOffset(mapFlr[2], data.playerPos)), getDistance(mapFlr[2], data.playerPos), mapFlr[2], data)[0],
                            data.cenY + getBend((getOffset(mapFlr[2], data.playerPos)), getDistance(mapFlr[2], data.playerPos), mapFlr[2], data)[1],
                            data.cenX + getBend((getOffset(mapFlr[3], data.playerPos)), getDistance(mapFlr[3], data.playerPos), mapFlr[3], data)[0],
                            data.cenY + getBend((getOffset(mapFlr[3], data.playerPos)), getDistance(mapFlr[3], data.playerPos), mapFlr[3], data)[1],
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
        self.y1 = y1
        self.y2 = y1 + length
        self.z1 = z1
        self.z2 = z1 + length
        self.face0 = ((self.x1, self.y1, self.z1), #bottom face
                      (self.x2, self.y1, self.z1),
                      (self.x2, self.y2, self.z1),
                      (self.x1, self.y2, self.z1))
        self.face1 = ((self.x1, self.y1, self.z1), #global left face
                      (self.x1, self.y2, self.z1),
                      (self.x1, self.y2, self.z2),
                      (self.x1, self.y1, self.z2))
        self.face2 = ((self.x1, self.y1, self.z2), #top face
                      (self.x2, self.y1, self.z2),
                      (self.x2, self.y2, self.z2),
                      (self.x1, self.y2, self.z2))
        self.face3 = ((self.x2, self.y1, self.z1), #global right face
                      (self.x2, self.y2, self.z1),
                      (self.x2, self.y2, self.z2),
                      (self.x2, self.y1, self.z2))
        self.face4 = ((self.x1, self.y2, self.z1), #global back face
                      (self.x2, self.y1, self.z2),
                      (self.x2, self.y2, self.z2),
                      (self.x1, self.y2, self.z2))
        self.face5 = ((self.x1, self.y1, self.z1), #global front face
                      (self.x2, self.y1, self.z1),
                      (self.x2, self.y1, self.z2),
                      (self.x1, self.y1, self.z2))
        self.faces = (self.face0, self.face1, self.face2, self.face3, 
                        self.face4, self.face5)
    def draw(self, canvas, data):
        for i in self.faces:
            canvas.create_polygon(data.cenX + getBend((getOffset(i[0], data.playerPos)), getDistance(i[0], data.playerPos), i[0], data)[0], 
                            data.cenY + getBend((getOffset(i[0], data.playerPos)), getDistance(i[0], data.playerPos), i[0], data)[1],
                            data.cenX + getBend((getOffset(i[1], data.playerPos)), getDistance(i[1], data.playerPos), i[1], data)[0],
                            data.cenY + getBend((getOffset(i[1], data.playerPos)), getDistance(i[1], data.playerPos), i[1], data)[1],
                            data.cenX + getBend((getOffset(i[2], data.playerPos)), getDistance(i[2], data.playerPos), i[2], data)[0],
                            data.cenY + getBend((getOffset(i[2], data.playerPos)), getDistance(i[2], data.playerPos), i[2], data)[1],
                            data.cenX + getBend((getOffset(i[3], data.playerPos)), getDistance(i[3], data.playerPos), i[3], data)[0],
                            data.cenY + getBend((getOffset(i[3], data.playerPos)), getDistance(i[3], data.playerPos), i[3], data)[1],
                            fill = "grey", outline = "grey")

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