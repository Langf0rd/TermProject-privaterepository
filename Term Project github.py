###########################################
# Vinay Mitta, vmitta, Section J
###########################################

# events-example0.py
# Barebones timer, mouse, and keyboard events taken from 
# https://www.cs.cmu.edu/~112/notes/hw5.html

from tkinter import *
import math
import random

def init(data):
    data.cenX = data.width/2
    data.cenY = data.height/2
    data.mode = "title"
    data.cubeSpread = 20000
    data.deathSpread = 1200
    data.cubeDist = 200000
    data.cubeWidth = 2000
    data.timerCount = 0
    data.speed = 3000
    data.movSpeed = 200
    data.cubeRate = 3
    data.startHeight = 1500
    data.playerPos = [0, 0, data.startHeight, 0, 0]
    data.jumpVel = 0
    data.lookVel = 0
    data.slideVel = 0
    data.gravity = -100
    data.antigravity = 100
    data.lookReturn = 0.1
    data.cubes = []
    data.score = 0
    data.colours = ("grey", "blue", "green", "dark blue", 
                    "light blue", "light green")
    data.cubeHeights = (0, 0, 0, 0, 1500, 1500)
    data.cubeWidths = (data.cubeWidth, data.cubeWidth, data.cubeWidth, 
                        data.cubeWidth, data.cubeWidth*2, data.cubeWidth*2, 
                        data.cubeWidth*3)

def jump(data):
    data.jumpVel = 600

def slide(data):
    data.lookVel = -0.5
    data.slideVel = -500

def drawDead(canvas, data):
    canvas.create_text(data.width/2, data.height/2, 
                        text = "Game Over", font = "Arial 25 bold")
    canvas.create_text(data.width/2, data.height/1.5,
                        text = "Press 'space' to restart", font = "Arial 15")

def removePassed(data):
    if data.cubes[-1].getCenter()[1] < data.playerPos[1]:
        data.cubes.pop()

def checkDeath(data):
    if ((abs(data.cubes[-1].getCenter()[0] - data.playerPos[0]) 
                < data.deathSpread) and 
        (abs(data.cubes[-1].getCenter()[1] - data.playerPos[1]) 
                <= data.speed) and
        (abs(data.cubes[-1].getCenter()[2] - data.playerPos[2]) 
                < data.deathSpread)):
        data.mode = "dead"

def drawTitle(canvas, data):
    canvas.create_text(data.width/2, data.height/5, 
                text = "Welcome To CubeRunner", font = "Arial 20 bold")
    canvas.create_text(data.width/2, data.height/2,
                text = "To start playing, press 'space'", 
                font = "Arial 15 bold")
    canvas.create_text(data.width/2, data.height/1.5,
                text = "For help press 'H'", 
                font = "Arial 15 bold")

def drawCubes(canvas, data):
    for i in data.cubes:
        i.draw(canvas, data)

def generateCubes(data):
    colour = data.colours[random.randint(0,5)]
    if data.score < 1000:
        height = 0
    else:
        height = data.cubeHeights[random.randint(0,5)]
    if data.score < 2000:
        width = data.cubeWidth
    else:
        width = data.cubeWidths[random.randint(0,6)]
    data.cubes.insert(0, cube(data.playerPos[0] + 
                        random.randint(-data.cubeSpread, data.cubeSpread),
                        data.playerPos[1] + data.cubeDist, height, data.cubeWidth, 
                        colour))

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    if data.mode == "playing":
        playingKeyPressed(event, data)
    if data.mode == "title":
        titleKeyPressed(event, data)
    if data.mode == "dead":
        deadKeyPressed(event, data)

def playingKeyPressed(event, data):
    # Need to change so its when pressed not single press
    if event.keysym == "w":
        data.playerPos[1] += data.movSpeed*math.cos(math.radians((data.playerPos[3])))
        data.playerPos[0] += data.movSpeed*math.sin(math.radians((data.playerPos[3])))
    #if event.keysym == "s":
    #    data.playerPos[1] += data.movSpeed*math.cos(math.radians((data.playerPos[3] + 180)))
    #    data.playerPos[0] += data.movSpeed*math.sin(math.radians((data.playerPos[3] + 180)))
    if event.keysym == "d" and data.playerPos[2] == data.startHeight:
        data.playerPos[1] += data.movSpeed*math.cos(math.radians((data.playerPos[3] + 270)))
        data.playerPos[0] += data.movSpeed*math.sin(math.radians((data.playerPos[3] + 270)))
    if event.keysym == "a" and data.playerPos[2] == data.startHeight:
        data.playerPos[1] += data.movSpeed*math.cos(math.radians((data.playerPos[3] + 90)))
        data.playerPos[0] += data.movSpeed*math.sin(math.radians((data.playerPos[3] + 90)))
    if event.keysym == 'space' and data.playerPos[2] == data.startHeight:
        jump(data)
    if event.keysym == 's' and data.playerPos[2] == data.startHeight:
        slide(data)
    #if event.keysym == "Up":
    #    if data.playerPos[4] < 60:
    #        data.playerPos[4] += 1 # Need to change it to the mouse movement
    #if event.keysym == "Down":
    #    if data.playerPos[4] > -60:
    #        data.playerPos[4] -= 1
    #if event.keysym == "Left":
    #    data.playerPos[3] += 1
    #    if data.playerPos[3] == 90 or data.playerPos[3] == 270:
    #        data.playerPos[3] += 1
    #if event.keysym == "Right":
    #    data.playerPos[3] -= 1
    #    if data.playerPos[3] == 90 or data.playerPos[3] == 270:
    #        data.playerPos[3] -= 1

def titleKeyPressed(event, data):
    if event.keysym == "space":
        data.mode = "playing"
    if event.keysym == "h":
        data.mode = "help"

def deadKeyPressed(event, data):
    if event.keysym == "space":
        init(data)

def timerFired(data):
    if data.mode == "playing":
        data.timerCount += 1
        if data.timerCount == data.cubeRate:
            data.timerCount = 0
        if data.timerCount == 1:
            generateCubes(data)
        data.score += (data.speed//1000)
        data.speed += 10
    if data.slideVel < 0 or data.playerPos[2] < data.startHeight:
        data.playerPos[2] += data.slideVel
    if data.slideVel < 1000:
        data.slideVel += data.antigravity
    if data.lookVel < 0 or data.playerPos[4] < 0:
        data.playerPos[4] += data.lookVel
    if data.lookVel < 5:
        data.lookVel += data.lookReturn
    if data.jumpVel > 0 or data.playerPos[2] > data.startHeight:
        data.playerPos[2] += data.jumpVel
    if data.jumpVel > -1000:
        data.jumpVel += data.gravity
    if data.mode == "playing" or data.mode == "dead":
        data.playerPos[1] += data.speed
        removePassed(data)
        checkDeath(data)
    if data.mode == "dead":
        data.speed = data.speed / 1.3
    print(data.playerPos[2])

def redrawAll(canvas, data):
    if data.mode == "playing" or data.mode == "dead":
        drawCubes(canvas, data)
        drawScore(canvas, data)
        drawCrosshairs(canvas, data)
    if data.mode == "dead":
        drawDead(canvas, data)
    elif data.mode == "title":
        drawTitle(canvas, data)
    elif data.mode == "help":
        drawHelp(canvas, data)

def drawHelp(canvas, data):
    canvas.create_text(data.width/2, data.height/5, 
                        text = "help")

def drawScore(canvas, data):
    canvas.create_text(data.width/6, data.height/8, 
                        text = "Score = "+str(data.score), font = "Arial 15",
                        anchor = "w")

def drawCrosshairs(canvas, data):
    canvas.create_rectangle(data.cenX - 30, data.cenY - 30,
                            data.cenX + 30, data.cenY + 30,
                            dash = (3,5))

def getBend(offset, distance, point, data):
    xBen = (offset[0]/(distance/1200))
    yBen = (offset[1]/((((distance**2) - 
            ((data.playerPos[2] - point[2])**2))**0.5)/1200))
    x = (data.playerPos[0] - point[0])
    y = (data.playerPos[1] - point[1])
    return (xBen, yBen)

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
    def __init__(self, x1, y1, z1, length, colour = "grey"):
        self.x1 = x1
        self.x2 = x1 + length
        self.y1 = y1
        self.y2 = y1 + length
        self.z1 = z1
        self.z2 = z1 + length
        self.length = length
        self.colour = colour
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
            canvas.create_polygon(
                data.cenX + getBend((getOffset(i[0], data.playerPos)), 
                    getDistance(i[0], data.playerPos), i[0], data)[0], 
                data.cenY + getBend((getOffset(i[0], data.playerPos)), 
                    getDistance(i[0], data.playerPos), i[0], data)[1],
                data.cenX + getBend((getOffset(i[1], data.playerPos)), 
                    getDistance(i[1], data.playerPos), i[1], data)[0],
                data.cenY + getBend((getOffset(i[1], data.playerPos)), 
                    getDistance(i[1], data.playerPos), i[1], data)[1],
                data.cenX + getBend((getOffset(i[2], data.playerPos)), 
                    getDistance(i[2], data.playerPos), i[2], data)[0],
                data.cenY + getBend((getOffset(i[2], data.playerPos)), 
                    getDistance(i[2], data.playerPos), i[2], data)[1],
                data.cenX + getBend((getOffset(i[3], data.playerPos)), 
                    getDistance(i[3], data.playerPos), i[3], data)[0],
                data.cenY + getBend((getOffset(i[3], data.playerPos)), 
                    getDistance(i[3], data.playerPos), i[3], data)[1],
                            fill = self.colour, outline = self.colour)
    def getCenter(self):
        return (self.x1 + (self.length/2), self.y1 + (self.length/2),
                    self.z1 + (self.length/2))

####################################
# Run Function
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
    data.timerDelay = 50 # milliseconds
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

run(720, 720)