from tkinter import *
from array import *
from time import *
import math
import random
from PIL import Image, ImageTk

totalParticles = 0
particlesOnScreen = 0
canvHeight =600
canvWidth = 1280
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
listOfColors = ["white", "green", "red", "yellow", "skyblue",
                "#baeb34", "#53eb34", "#badbcf", "#64a1b3", "#d000ff", "#ff00bf"]

frameLeft = Frame(t, width=30)
frameLeft.pack(side=LEFT)

lbl = Label(frameLeft, text = "Max X var ", font=("Segoe UI Bold", 20))
lbl.pack(side=LEFT)

xDiff= Entry(frameLeft, bd =5, font=("Segoe UI Bold", 20), width=5)
xDiff.insert(0, "0.5")
xDiff.pack(side=LEFT)

frameMid = Frame(t)
frameMid.pack(side=LEFT)

lbl = Label(frameLeft, text = "   Max particles ", font=("Segoe UI Bold", 20))
lbl.pack(side=LEFT) 

maxParticles= Entry(frameLeft, bd =5, font=("Segoe UI Bold", 20), width=5)
maxParticles.insert(0, "52")
maxParticles.pack(side=LEFT)

frame = Frame(t)
frame.pack(side=RIGHT)

lbl = Label(frame, text = "    Min/Max Y var ", font=("Segoe UI Bold", 20))
lbl.pack(side=LEFT)

yDiffMin = Entry(frame, bd =5, font=("Segoe UI Bold", 20), width=5)
yDiffMin.insert(0, "-1.0")
yDiffMin.pack(side=LEFT)

yDiffMax = Entry(frame, bd =5, font=("Segoe UI Bold", 20), width=5)
yDiffMax.insert(0, "3.0")
yDiffMax.pack(side=LEFT)

lblTotal = c.create_text(canvWidth/2, 20, text = "Total cloned: " + str(totalParticles), font=("Segoe UI Bold", 20), fill="white")

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
    global totalParticles, particlesOnScreen
    randomX = random.randrange(50, canvWidth-50)
    randomY = random.randrange(500, 575)
    particleSz = random.randrange(6,  12)
    spd = random.randrange(8, 13)
    sldown = random.uniform(0.1, 0.15)
    particle = c.create_rectangle(randomX, randomY, randomX+particleSz, randomY+particleSz, fill="white")
    totalParticles +=1
    particlesOnScreen+=1
    listOfParticles.append(particle)
    particleSpeed.append(spd)
    particleSize.append(particleSz)
    particleSlowdown.append(sldown)
    particleLoop.append(0)
    particleBroke.append(False)

def createExplosion(num, spread, xPos, yPos, size, decrement, spiral, spiralIncrement):
    global totalParticles, particlesOnScreen
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
        totalParticles +=1
        particlesOnScreen +=1
        circularX = xPos + spread*math.cos(i*increment + (3*math.pi/2))
        circularY = yPos + spread*math.sin(i*increment + (3*math.pi/2))
        #c.create_rectangle(circularX, circularY, circularX+15, circularY+15, fill="white")
        clonedRect = c.create_oval(circularX-(size/2), circularY-(size/2), circularX+(size/2), circularY+(size/2), fill= randomColor)
        subClonedParticles.append(clonedRect)
        subClonedParticlesSpread.append(i*increment + (3*math.pi/2))#appending angle
        if(xDiff.get() == "" or xDiff.get() == " "):
            subClonedParticlesVariationX.append(0)
        else:
            subClonedParticlesVariationX.append(random.uniform(0-float(xDiff.get()), float(xDiff.get())))#-0.5, 0.5

        if(yDiffMin.get() == "-" or yDiffMin.get() == "" or yDiffMax.get() == "-" or yDiffMax.get() == ""):
             subClonedParticlesVariationY.append(0)
        else:
            subClonedParticlesVariationY.append(random.uniform(float(yDiffMin.get()), float(yDiffMax.get())))#-1.0, 3.0
        
    clonedParticles.append(subClonedParticles)
    clonedParticlesSpread.append(subClonedParticlesSpread)
    clonedParticlesVariationX.append(subClonedParticlesVariationX)
    clonedParticlesVariationY.append(subClonedParticlesVariationY)
   
def moveSingleParticles():
    global particlesOnScreen
    for i in range (len(listOfParticles)):
        c.move(listOfParticles[i], 0, 0-(particleSpeed[i] - (particleSlowdown[i]*particleLoop[i])))
        #c.move(listOfParticles[i], 0, -10)
        particleLoop[i] += 1;

        if (particleSpeed[i] - (particleSlowdown[i]*particleLoop[i]) < 2 and not particleBroke[i]):
            if (random.randrange(1, 2) == 1):
                if(maxParticles.get() == "" or int(maxParticles.get()) <= 20 ):
                    createExplosion(random.randrange(20,52), 4, c.coords(listOfParticles[i])[0]+(particleSize[i]/2),
                    c.coords(listOfParticles[i])[1]+(particleSize[i]/2), particleSize[i], particleSlowdown[i], True, random.uniform(0.10, 3.14))
                else:
                    createExplosion(random.randrange(20, int(maxParticles.get())), 4, c.coords(listOfParticles[i])[0]+(particleSize[i]/2),
                    c.coords(listOfParticles[i])[1]+(particleSize[i]/2), particleSize[i], particleSlowdown[i], True, random.uniform(0.10, 3.14))
            else:
                if(maxParticles.get() == "" or int(maxParticles.get()) <= 20):
                    createExplosion(random.randrange(20, 52), 4, c.coords(listOfParticles[i])[0]+(particleSize[i]/2),
                    c.coords(listOfParticles[i])[1]+(particleSize[i]/2), particleSize[i], particleSlowdown[i], False, -1)
                else:
                    createExplosion(random.randrange(20, int(maxParticles.get())), 4, c.coords(listOfParticles[i])[0]+(particleSize[i]/2),
                    c.coords(listOfParticles[i])[1]+(particleSize[i]/2), particleSize[i], particleSlowdown[i], False, -1)
            
            particleBroke[i] = True
            c.delete(listOfParticles[i])
            particlesOnScreen -=1
        

def moveClonedParticles():
   for i in range (len(clonedParticles)):
       for j in range (len(clonedParticles[i])):
           c.move(clonedParticles[i][j], (math.cos(clonedParticlesSpread[i][j])*1.75 + clonedParticlesVariationX[i][j]),
           0-(particleSpeed[i] - (particleSlowdown[i]*particleLoop[i]*1)+(math.sin(clonedParticlesSpread[i][j]))+clonedParticlesVariationY[i][j]))
    #for i in range(len(listOfParticles)):

def deleteParticles():
    #print("Before: ", clonedParticles)
    global particlesOnScreen
    i = 0
    j = 0
    
    while (i < len(clonedParticles)):
        j = 0
        initial = len(clonedParticles[i])
        while (j < len(clonedParticles[i])):
            if(c.coords(clonedParticles[i][j])[0] < 0 or c.coords(clonedParticles[i][j])[0] > canvWidth or c.coords(clonedParticles[i][j])[1] > canvHeight):
               c.delete(clonedParticles[i][j])
               clonedParticles[i].pop(j)
               clonedParticlesSpread[i].pop(j)
               clonedParticlesVariationX[i].pop(j)
               clonedParticlesVariationY[i].pop(j)
               j = j -1
               
            j +=1
        i+=1
        particlesOnScreen -= initial - j
        
while True:
    if(random.randrange(1, 80) == 1):
        createInitialParticle()
    moveSingleParticles()
    moveClonedParticles()
    deleteParticles()
    c.itemconfig (lblTotal, text = "Total cloned: " + str(totalParticles) + " | On screen: " + str(particlesOnScreen))
    t.update()
    sleep(0.001)
 
   
    

