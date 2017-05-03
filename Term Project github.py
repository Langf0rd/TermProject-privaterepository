###########################################
# Vinay Mitta, vmitta, Section J
###########################################

# events-example0.py
# Barebones timer, mouse, and keyboard events taken from 
# https://www.cs.cmu.edu/~112/notes/hw5.html

from tkinter import *
import math
import random

#####################################
# Init functions
#####################################

def init(data):
    data.cenX = data.width/2 # Gets the center of the screen x and y values
    data.cenY = data.height/2
    initSettings(data)
    initDefaults(data)
    initHelp(data)

# Initialises values that do not change during gameplay
def initSettings(data):
    data.cubeSpread = 20000
    data.deathSpread = 1600 # This distance from cube center = collision
    data.cubeDist = 200000
    data.cubeWidth = 2000
    data.movSpeed = 800
    data.cubeRate = 3 # Determines how often a cube is generated
    data.startHeight = 1500
    data.gravity = -100 # Used to return the player to ground level when jumping
    data.antigravity = 100 # Same as above but used for sliding
    data.lookReturn = 0.1 # Used to pull the camera view back to center
    # data.colours and data.cubeHeights are used to randomize the cubes
    data.colours = ("yellow", "blue", "green", "dark blue", 
                    "light blue", "light green", "maroon", "red")
    data.cubeHeights = (0, 0, 0, 0, 0, 0, 1500, 1500)

# Initialises values that will be changed during gameplay
def initDefaults(data):
    data.score = 0
    data.timerCount = 0
    data.mode = "title"
    data.playerPos = [0, 0, data.startHeight, 0, 0]
    data.right = False # Is the player moving right/left
    data.left = False
    data.scored = 0 
    data.cubes = [] # List is updated with all the cubes on screen
    data.jumpVel = 0
    data.lookVel = 0
    data.slideVel = 0
    data.speed = 3000

# Initialises everything used for the help screen
def initHelp(data):
    data.redHelpCube = cube(-5000, 45000, 1500, data.cubeWidth, "red")
    data.darkRedHelpCube = cube(-6000, 35000, 1400, data.cubeWidth, "maroon")
    data.yellowHelpCube = cube(1000, 20000, -1500, data.cubeWidth, "yellow")

#####################################
# Action and gameplay functions
#####################################

# For jump and slide, when the Vel values are changed the gravity values
# pull the player back towards the ground
def jump(data):
    data.jumpVel = 600

def slide(data):
    data.lookVel = -0.5
    data.slideVel = -500

def moveRight(data):
    data.playerPos[1] += (data.movSpeed+data.speed/50)*math.cos(math.radians(
                                                (data.playerPos[3] + 270)))
    data.playerPos[0] += (data.movSpeed+data.speed/50)*math.sin(math.radians(
                                                (data.playerPos[3] + 270)))

def moveLeft(data):
    data.playerPos[1] += (data.movSpeed+data.speed/50)*math.cos(math.radians(
                                                (data.playerPos[3] + 90)))
    data.playerPos[0] += (data.movSpeed+data.speed/50)*math.sin(math.radians(
                                                (data.playerPos[3] + 90)))

def removePassed(data):
    if data.cubes[-1].getCenter()[1] < data.playerPos[1]:
        data.cubes.pop()

# Checks if the player has collided with a cube and either sets to game over
# or gives points accordingly
def checkDeath(data):
    if ((abs(data.cubes[-1].getCenter()[0] - data.playerPos[0]) 
                < data.deathSpread) and 
        (abs(data.cubes[-1].getCenter()[1] - data.playerPos[1]) 
                <= data.speed) and
        (abs(data.cubes[-1].getCenter()[2] - data.playerPos[2]) 
                < data.deathSpread)):
        if data.cubes[-1].getColour() == "yellow":
            data.score += 100
            data.scored = 10
        else:
            data.mode = "dead"

def generateCubes(data):
    if data.score < 1000:
        height = 0
        colour = data.colours[random.randint(0,5)]
    else:
        select = random.randint(0,7)
        height = data.cubeHeights[select]
        colour = data.colours[select]
    data.cubes.insert(0, cube(data.playerPos[0] + 
                        random.randint(-data.cubeSpread, data.cubeSpread),
                        data.playerPos[1] + data.cubeDist, height, 
                        data.cubeWidth, colour))

# getBend is used to determing the 'bend' based on how far away an object is
# from the player and then pushes the display of that object towards the center
# of the screen to simulate objects in the distance appearing smaller
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

# Finds the left/right and up/down offset of an object from the player based on
# both the players position and which direction the player is facing
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

#####################################
# Keypress functions
#####################################

def mousePressed(event, data):
    pass

def keyPressed(event, data):
    if data.mode == "playing":
       #playingKeyPressed(event, data)
       keyDown(event, data)
    if data.mode == "title":
        titleKeyPressed(event, data)
    if data.mode == "dead":
        deadKeyPressed(event, data)
    if data.mode == "help":
        if event.keysym == 'space':
            data.mode = "title"

def playingKeyPressed(event, data):
    # The left and right movement allows for roatation of the camera
    # so if the player was not facing forward they would move left and right 
    # based on where they were facing and not based on the maps x/y orientation
    if event.keysym == "Right" and data.playerPos[2] == data.startHeight:
        data.playerPos[1] += data.movSpeed*math.cos(math.radians(
                                            (data.playerPos[3] + 270)))
        data.playerPos[0] += data.movSpeed*math.sin(math.radians(
                                            (data.playerPos[3] + 270)))
    if event.keysym == "Left" and data.playerPos[2] == data.startHeight:
        data.playerPos[1] += data.movSpeed*math.cos(math.radians(
                                            (data.playerPos[3] + 90)))
        data.playerPos[0] += data.movSpeed*math.sin(math.radians(
                                            (data.playerPos[3] + 90)))
    if event.keysym == "Up" and data.playerPos[2] == data.startHeight:
        jump(data)
    if event.keysym == "Down" and data.playerPos[2] == data.startHeight:
        slide(data)

def keyDown(event, data):
    if event.keysym == "Right":
        data.right = True
    if event.keysym == "Left":
        data.left = True
    if event.keysym == 'Up' and data.playerPos[2] == data.startHeight:
        jump(data)
    if event.keysym == 'Down' and data.playerPos[2] == data.startHeight:
        slide(data)

def keyReleased(event, data):
    if data.mode != "playing":
        pass
    if event.keysym == "Right":
        data.right = False
    if event.keysym == "Left":
        data.left = False

def titleKeyPressed(event, data):
    if event.keysym == "space":
        data.mode = "playing"
    if event.keysym == "h":
        data.mode = "help"

def deadKeyPressed(event, data):
    if event.keysym == "space":
        init(data)

#####################################
# Draw functions
#####################################

# Draws game over screen
def drawDead(canvas, data):
    canvas.create_text(data.width/2, data.height/2, 
                        text = "Game Over", font = "Arial 25 bold")
    canvas.create_text(data.width/2, data.height/1.5,
                        text = "Press 'space' to restart", font = "Arial 15")

def drawTitle(canvas, data):
    canvas.create_text(data.width/2, data.height/5, 
                text = "Welcome To CubeRunner", font = "Arial 20 bold")
    canvas.create_text(data.width/2, data.height/2,
                text = "To start playing, press 'space'", 
                font = "Arial 15 bold")
    canvas.create_text(data.width/2, data.height/1.5,
                text = "For help or instructions press 'H'", 
                font = "Arial 15 bold")

# Draws all the cubes in the list of current cubes
def drawCubes(canvas, data):
    for i in data.cubes:
        i.draw(canvas, data)

# Draws the indicators that tell the player they hit a yellow block
def drawScored(canvas, data):
    canvas.create_rectangle(0,0, data.width, data.height, fill = "light yellow")
    canvas.create_text(data.width/2, data.height/5, text = "score + 100",
                        font = "Arial 20")

# Draws the grey floor and horizon
def drawHorizon(canvas, data):
    data.horizon = cube(data.playerPos[0] - 100000, data.playerPos[1] + 230000,
                        -180000, 180000, "light grey")
    data.horizon.draw(canvas, data)

# Draws the help screen
def drawHelp(canvas, data):
    canvas.create_text(data.width/2, data.height/10, 
                        text = "Instructions", font = "Arial 15 bold")
    canvas.create_text(data.width/2, data.height/5,
                        text = "Welcome to CubeRunner!\n\nUse the arrow keys"+
                                " to move around\n'Left' and 'Right' to "+
                                "move side to side, 'Up' to jump and 'Down'"+
                            " to slide",
                        font = "Arial 10", justify = "center")
    canvas.create_text(data.width/2, data.height/3,
                        text = ("Avoid cubes to stay alive for as long as" + 
                                " possible"),
                        font = "Arial 10 bold", justify = "center")
    canvas.create_text(data.width/3, data.height/2,
                        text = ("You can jump over most cubes and can't"+
                                " slide under them,\n but it is the opposite"+
                                " for the red and dark red floating cubes"),
                        font = "Arial 10", justify = "center")
    canvas.create_text(2*data.width/3, 2*data.height/3,
                        text = ("Yellow cubes will give you extra points!!,\n"+
                                "so try and hit as many as you can"),
                        font = "Arial 10", justify = "center")
    data.redHelpCube.draw(canvas, data)
    data.darkRedHelpCube.draw(canvas, data)
    data.yellowHelpCube.draw(canvas, data)
    canvas.create_text(data.width/2, 5*data.height/6,
                        text = "Press 'space' to return to menu",
                        font = "Arial 10 bold")

# Draws the players score in the top left
def drawScore(canvas, data):
    canvas.create_text(data.width/6, data.height/8, 
                        text = "Score = "+str(data.score), font = "Arial 15",
                        anchor = "w")

# Used for testing to see how movement and scaling works

#def drawCrosshairs(canvas, data):
#    canvas.create_rectangle(data.cenX - 30, data.cenY - 30,
#                            data.cenX + 30, data.cenY + 30,
#                            dash = (3,5))

#####################################
# Animation functions
#####################################

def timerFired(data):
    if data.mode == "playing":
        playingTimerFired(data)
    if data.mode == "playing" or data.mode == "dead":
        data.playerPos[1] += data.speed
        removePassed(data)
        checkDeath(data)
        if data.scored > 0:
            data.scored -= 1
    if data.mode == "dead":
        data.speed = data.speed / 1.3
    if data.left == True:
        moveLeft(data)
    if data.right == True:
        moveRight(data)

def playingTimerFired(data):
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

def redrawAll(canvas, data):
    if data.mode == "playing" or data.mode == "dead":
        if data.scored > 0:
            drawScored(canvas, data)
        drawHorizon(canvas, data)
        drawCubes(canvas, data)
        drawScore(canvas, data)
        #drawCrosshairs(canvas, data)
    if data.mode == "dead":
        drawDead(canvas, data)
    elif data.mode == "title":
        drawTitle(canvas, data)
    elif data.mode == "help":
        drawHelp(canvas, data)

#####################################
# Cube class
#####################################

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
    # Draws the cubes using their positions, offsets from the player
    # and the 'bend' calculated from the distance they are from the player
    def draw(self, canvas, data):
        for i in self.faces: # draws each face of each cube
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
    def getColour(self):
        return self.colour

####################################
# Run Function
####################################

def run(width=720, height=720): # Default screen set to 720x720
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

    def keyReleasedWrapper(event, canvas, data):
        keyReleased(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 50 # ms (adjusted to increase effective framerate)
    init(data)
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<KeyRelease>", lambda event: # Allows for functions to be tied
                                            # to whenever a key is help down
                            keyReleasedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    root.mainloop() 
    print("bye!")

run(720, 720) # Screen size set to 720x720

############################################
# Spare Code
############################################

# Spare keypressed code that allows for rotation of the camera which I may
# use in the future so I'm holding on to it

#if event.keysym == "w":
    #    data.playerPos[1] += data.movSpeed*math.cos(math.radians(
    #                                                (data.playerPos[3])))
    #    data.playerPos[0] += data.movSpeed*math.sin(math.radians(
    #                                                (data.playerPos[3])))
    #if event.keysym == "s":
    #    data.playerPos[1] += data.movSpeed*math.cos(math.radians(
    #                                                (data.playerPos[3] + 180)))
    #    data.playerPos[0] += data.movSpeed*math.sin(math.radians(
    #                                               (data.playerPos[3] + 180)))

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