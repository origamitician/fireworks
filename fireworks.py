from tkinter import *
from array import *
from time import *
import math
import random
from PIL import Image, ImageTk

canvHeight = 600
canvWidth = 500
t=Tk()
c = Canvas(t, height=canvHeight, width=canvWidth)
c.pack()
c.create_rectangle(0, 0, canvWidth, canvHeight, fill="black")
listOfParticles = []
particleSpeed = []
particleSlowdown = []
particleLoop = []
particleSize = []
particleBroke = []
images = []  # to hold the newly created image
needToDelete = -1
clonedParticles = []
clonedParticlesSpread = []
clonedParticlesVariationX = []
clonedParticlesVariationY = []
listOfColors = ["white", "green", "red", "yellow", "skyblue", "lightgreen"]

#totally did NOT copy this from stackoverflow
def create_transparent_rectangle(x1, y1, x2, y2, **kwargs):
    if 'alpha' in kwargs:
        print('alpha exists')
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = t.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (x2-x1, y2-y1), fill)
        images.append(ImageTk.PhotoImage(image))
        c.create_image(x1, y1, image=images[-1], anchor='nw')
    c.create_rectangle(x1, y1, x2, y2, **kwargs)
    
def createInitialParticle():
    randomX = random.randrange(50, canvWidth-50)
    randomY = random.randrange(500, 575)
    particleSz = random.randrange(4, 8)
    spd = random.randrange(7, 13)
    sldown = random.uniform(0.1, 0.2)
    particle = c.create_rectangle(randomX, randomY, randomX+particleSz, randomY+particleSz, fill="white")
    
    listOfParticles.append(particle)
    particleSpeed.append(spd)
    particleSize.append(particleSz)
    particleSlowdown.append(sldown)
    particleLoop.append(0)
    particleBroke.append(False)

def createExplosion(num, spread, xPos, yPos, size, decrement, spiral, spiralIncrement):
    subClonedParticles = []
    subClonedParticlesSpread = []
    subClonedParticlesVariationX = []
    subClonedParticlesVariationY = []
    randomColor = listOfColors[random.randrange(0, len(listOfColors)-1)]
    if(not spiral):
        increment = 2*math.pi / num
    else:
        increment= spiralIncrement
    for i in range (num):
        circularX = xPos + spread*math.cos(i*increment + (3*math.pi/2))
        circularY = yPos + spread*math.sin(i*increment + (3*math.pi/2))
        #c.create_rectangle(circularX, circularY, circularX+15, circularY+15, fill="white")
        clonedRect = c.create_oval(circularX-(size/2), circularY-(size/2), circularX+(size/2), circularY+(size/2), fill= randomColor)
        subClonedParticles.append(clonedRect)
        subClonedParticlesSpread.append(i*increment + (3*math.pi/2))#appending angle
        subClonedParticlesVariationX.append(random.uniform(-0.5, 0.5))
        subClonedParticlesVariationY.append(random.uniform(-1.0, 3.0))
        #sleep(0.1)
        #t.update()
    clonedParticles.append(subClonedParticles)
    clonedParticlesSpread.append(subClonedParticlesSpread)
    clonedParticlesVariationX.append(subClonedParticlesVariationX)
    clonedParticlesVariationY.append(subClonedParticlesVariationY)
   
def moveSingleParticles():
    global needToDelete
    for i in range (len(listOfParticles)):
        c.move(listOfParticles[i], 0, 0-(particleSpeed[i] - (particleSlowdown[i]*particleLoop[i])))
        #c.move(listOfParticles[i], 0, -10)
        particleLoop[i] += 1;

        if (particleSpeed[i] - (particleSlowdown[i]*particleLoop[i]) < 2 and not particleBroke[i]):
            if (random.randrange(1, 2) == 1):
                createExplosion(random.randrange(20, 52), 4, c.coords(listOfParticles[i])[0]+(particleSize[i]/2),
                c.coords(listOfParticles[i])[1]+(particleSize[i]/2), particleSize[i], particleSlowdown[i], True, 0.38)
            else:
                createExplosion(random.randrange(20, 52), 4, c.coords(listOfParticles[i])[0]+(particleSize[i]/2),
                c.coords(listOfParticles[i])[1]+(particleSize[i]/2), particleSize[i], particleSlowdown[i], False, -1)
            
            particleBroke[i] = True
            c.itemconfig(listOfParticles[i], state=HIDDEN)
            #needToDelete = i   
        #del (particleSpeed[needToDelete])
        #del (particleSlowdown[needToDelete])
        #del (particleLoop[needToDelete])
        #del (particleSize[needToDelete])
        #del (particleBroke[needToDelete])

def moveClonedParticles():
   for i in range (len(clonedParticles)):
       for j in range (len(clonedParticles[i])):
           c.move(clonedParticles[i][j], (math.cos(clonedParticlesSpread[i][j])*1.75 + clonedParticlesVariationX[i][j]),
           0-(particleSpeed[i] - (particleSlowdown[i]*particleLoop[i]*1)+(math.sin(clonedParticlesSpread[i][j]))+clonedParticlesVariationY[i][j]))
    #for i in range(len(listOfParticles)):

def deleteParticles():
    for i in range (len(clonedParticles)):
       for j in range (len(clonedParticles[i])):
           if(c.coords(clonedParticles[i][j])[0] < 0 or c.coords(clonedParticles[i][j])[0] > canvWidth or c.coords(clonedParticles[i][j])[1] > canvHeight):
               c.delete(clonedParticles[i][j])
               clonedParticlesSpread[i].pop(j)
               clonedParticlesVariationX[i].pop(j)
               clonedParticlesVariationY[i].pop(j)
    
while True:
    if(random.randrange(1, 35) == 1):
        createInitialParticle()
    moveSingleParticles()
    moveClonedParticles()
    #deleteParticles()
    t.update()
    #sleep(0.0001)
    

