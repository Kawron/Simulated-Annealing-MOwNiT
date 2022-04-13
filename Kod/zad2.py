import copy
import random
import math
import time
import cv2
import numpy as np
from Node import Node
from simulatedAnnealing import previewSlope, runSimulations
import matplotlib.pyplot as plt
import imageio
import os

class BinaryNode(Node):
    
    def getRadious(self):
        maxi = -1
        for offset in self.offsets:
            maxi = max(maxi, abs(offset[0]))
            maxi = max(maxi, abs(offset[1]))
        return maxi

    def __init__(self, width, height, delta=0, offsets=[(-1,0),(1,0),(0,1),(1,0),(1,1),(-1,-1),(-1,1),(1,-1)], amount=0.01, reverseForce = False):
        self.width = width
        self.height = height
        self.delta = delta
        self.offsets = offsets
        self.amount = amount
        self.radious = self.getRadious()
        self.stack = []
        # affectedSet - set of points affected by swap
        # swapSet - points to be swapped after choosing them in loop in neighbour()
        self.affectedSet = set({})
        self.swapSet = set({})
        # change if black points atrract or repel each other
        self.reverseForce = reverseForce
        
        self.points = [[0 for _ in range(width)] for _ in range(height)]

        self.numOfPoints = math.floor(width*height*delta)
        for _ in range(self.numOfPoints):
            while 1:
                x = random.randint(0,width-1)
                y = random.randint(0,height-1)
                if self.points[x][y] != 0:
                    continue
                self.points[x][y] = 1
                break

        self.oldEnergy = self.initEnergy()
        self.currEnergy = self.initEnergy()

    def initEnergy(self):
        energy = 0
        for i in range(self.width):
            for j in range(self.height):
                energy += self.energyOfPoint(i,j)
        return energy

    def energyOfPoint(self, x, y):
        energy = 0
        if self.points[x][y] == 0:
            return energy
        for offset in self.offsets:
            newX = (x + offset[0]) % self.width
            newY = (y + offset[1]) % self.height
            if self.reverseForce == False:
                if self.points[newX][newY] != 0:
                    energy += 1
            else:
                if self.points[newX][newY] != 0:
                    energy -= 1
        return energy

    def deleteEnergy(self):
        test = 0
        localSet = copy.deepcopy(self.affectedSet)
        while len(localSet) != 0:
            point = localSet.pop()
            self.currEnergy -= self.energyOfPoint(point[0], point[1])
            test += self.energyOfPoint(point[0], point[1])

    def addEnergy(self):
        localSet = copy.deepcopy(self.affectedSet)
        while len(localSet) != 0:
            point = localSet.pop()
            self.currEnergy += self.energyOfPoint(point[0], point[1])


    def getEnergy(self):
        return self.currEnergy

    def getPointsInRadious(self, x, y):
        res = []
        for i in range(-self.radious, self.radious+1):
            for j in range(-self.radious, self.radious+1):
                newX = (x+i)%self.width
                newY = (y+j)%self.height
                res.append((newX, newY))
        return res


    def addToAffectedSet(self, vicinity):
        for point in vicinity:
            self.affectedSet.add(point)

    def neighbour(self, temp):
        # toSwap = math.floor(self.numOfPoints*self.amount)
        if temp > 0.4:
            toSwap = math.floor(self.numOfPoints*(self.amount*20))
        else:
            toSwap = math.floor(self.numOfPoints*self.amount)

        self.oldEnergy = self.currEnergy
        
        for _ in range(toSwap):
            x1 = random.randint(0,self.width-1)
            y1 = random.randint(0,self.height-1)
            x2 = random.randint(0,self.width-1)
            y2 = random.randint(0,self.height-1)
            pointVicinity1 = self.getPointsInRadious(x1, y1)
            pointVicinity2 = self.getPointsInRadious(x2, y2)
            self.addToAffectedSet(pointVicinity1)
            self.addToAffectedSet(pointVicinity2)
            self.swapSet.add((x1,y1,x2,y2))
        
        self.deleteEnergy()
        while len(self.swapSet) != 0:
            x1,y1,x2,y2= self.swapSet.pop()
            self.points[x1][y1], self.points[x2][y2] = self.points[x2][y2], self.points[x1][y1]
            self.stack.append((x1,y1,x2,y2))

        self.addEnergy()
        self.affectedSet.clear()
        self.swapSet.clear()

    def acceptState(self):
        while self.stack != []:
            self.stack.pop()

    def prevState(self):
        self.currEnergy = self.oldEnergy
        while self.stack != []:
            x1,y1,x2,y2 = self.stack.pop()
            self.points[x1][y1], self.points[x2][y2] = self.points[x2][y2], self.points[x1][y1]

    def screenShot(self):
        matrix = np.zeros((self.height,self.width,3), np.uint8)
        for i in range(self.width):
            for j in range(self.height):
                if self.points[i][j] == 0:
                    matrix[i,j] = (255,255,255)
                else:
                    matrix[i,j] = (0,0,0)
        return matrix

    def newStartPoint(self):
        return BinaryNode(self.width, self.height, self.delta, self.offsets, self.amount)

class ColorNode(BinaryNode):

    def __init__(self, width, height, delta=0, offsets=[(-1,0),(1,0),(0,1),(1,0),(1,1),(-1,-1),(-1,1),(1,-1)], amount=0.01):
        BinaryNode.__init__(self, width, height, delta, offsets, amount)
        
        for i in range(height):
            for j in range(width):
                self.points[j][i] = 0

        for _ in range(self.numOfPoints):
            while 1:
                x = random.randint(0,width-1)
                y = random.randint(0,height-1)
                color = random.randint(1,2)
                if self.points[x][y] != 0:
                    continue
                self.points[x][y] = color
                break

    def energyOfPoint(self, x, y):
        # R = 0, G = 1, B = 2
        energy = 0
        color = self.points[x][y]
        for offset in self.offsets:
            newX = (x + offset[0]) % self.width
            newY = (y + offset[1]) % self.height
            # te same sie przyciagaja inne odpychaja
            # czerwony odpycha, niebieski i zielony sie przyciągają
            if self.points[newX][newY] == color:
                energy -= 1
            elif self.points[newX][newY] == 0 or color == 0:
                energy += 1
            elif self.points[newX][newY] == 1 and color == 2:
                energy -= 1
            elif self.points[newX][newY] == 2 and color == 1:
                energy -= 1
        return energy

    def screenShot(self):
        matrix = np.zeros((self.height,self.width,3), np.uint8)
        for i in range(self.height):
            for j in range(self.width):
                color = self.points[i][j]
                # z jakiegoś powodu (0,0,255) to czerwony a nie niebieski
                match color:
                    case 0:
                        matrix[i,j] = (0,0,255)
                    case 1:
                        matrix[i,j] = (0,255,0)
                    case 2:
                        matrix[i,j] = (255,0,0)
        return matrix

    def newStartPoint(self):
        return ColorNode(self.width, self.height, self.delta, self.offsets, self.amount)

class SmoothColorNode(BinaryNode):
    
    def __init__(self, width, height, delta=0, offsets=[(-1,0),(1,0),(0,1),(1,0),(1,1),(-1,-1),(-1,1),(1,-1)], amount=0.01, displayColor="green"):
        BinaryNode.__init__(self, width, height, delta, offsets, amount)
        self.displayColor = displayColor

        for i in range(height):
            for j in range(width):
                self.points[j][i] = 0

        for _ in range(self.numOfPoints):
            while 1:
                x = random.randint(0,width-1)
                y = random.randint(0,height-1)
                color = random.randint(0,255)
                if self.points[x][y] != 0:
                    continue
                self.points[x][y] = color
                break

    def energyOfPoint(self, x, y):
        energy = 0
        color = self.points[x][y]
        # if color == 0:
        #     return 0
        for offset in self.offsets:
            newX = (x + offset[0]) % self.width
            newY = (y + offset[1]) % self.height
            # podobne kolory się przyciągają
            energy += abs(self.points[newX][newY] - color)
        return energy

    def screenShot(self):
        matrix = np.zeros((self.height,self.width,3), np.uint8)
        for i in range(self.width):
            for j in range(self.height):
                color = self.points[i][j]
                match self.displayColor:
                    case("green"):
                        matrix[i,j] = (0,color,0)
                    case("blue"):
                        matrix[i,j] = (color,0,0)
                    case("red"):
                        matrix[i,j] = (0,0,color)
        return matrix

    def newStartPoint(self):
        return SmoothColorNode(self.width, self.height, self.delta, self.offsets, self.amount, displayColor=self.displayColor)


def createGif(nodes, name):
    fileNames = []
    n = len(nodes)
    for i in range(n):
        cv2.imwrite(f"./{name}/{i}.png", nodes[i])
        fileNames.append(f"./{name}/{i}.png")
    name = name + "/" + name + ".gif"
    with imageio.get_writer(name, mode='I') as writer:
        for filename in fileNames:
            image = imageio.imread(filename)
            writer.append_data(image)

def elapseTime(startingNode, numOfRestarts, startTemp, maxIteration):
    start = time.time()
    runSimulations(startingNode,1,startTemp, maxIteration=200)
    end = time.time()
    res = (end-start) * numOfRestarts * maxIteration / 200
    print(f"Elapsed time is: {res/60} min")

def main(x):
    match x:
        case(1):
            # cross
            name = "cross" + str(random.randint(0,9000000))
            os.system("mkdir "+name)
            startingNode = BinaryNode(48,48,0.5,amount=0.003, offsets=[(-1,0),(1,0),(0,1),(1,0)])
            resArray, bestRes = runSimulations(startingNode, 5, 1, maxIteration=1000000, timeFactor=17500, probFactor=20, directory=name)
            createGif(resArray, name)
        case(2):
            # rogi
            name = "rogi" + str(random.randint(0,9000000))
            os.system("mkdir "+name)
            startingNode = BinaryNode(48,48,0.5,amount=0.003, offsets=[(1,1),(-1,-1),(-1,1),(1,-1)])
            resArray, bestRes = runSimulations(startingNode, 5, 1, maxIteration=1000000, timeFactor=17500, probFactor=20, directory=name)
            createGif(resArray, name)
        case(3):
            #skos
            name = "skos" + str(random.randint(0,9000000))
            os.system("mkdir "+name)
            startingNode = BinaryNode(48,48,0.5,amount=0.003, offsets=[(-1,-1),(1,1)])
            resArray, bestRes = runSimulations(startingNode, 5, 1, maxIteration=1000000, timeFactor=17500, probFactor=20, directory=name)
            createGif(resArray, name)
        case(4):
            # pierscien
            name = "pierscien" + str(random.randint(0,9000000))
            os.system("mkdir "+name)
            pattern = [(-2,-2),(-1,2),(0,2),(1,2),(2,2),(2,1),(2,0),(2,-1),(2,-2),(1,-2),(0,-2),(-1,-2),(-2,-2),(-2,-1),(-2,0),(-2,1),(-2,2)]
            startingNode = BinaryNode(48,48,0.5,amount=0.003, offsets=pattern)
            resArray, bestRes = runSimulations(startingNode, 5, 1, maxIteration=1000000, timeFactor=17500, probFactor=20, directory=name)
            createGif(resArray, name)
        case(5):
            # szachownica
            name = "szachownica" + str(random.randint(0,9000000))
            os.system("mkdir "+name)
            pattern = [(-1,-1),(-1,1),(1,-1),(1,1),(-2,2),(2,2),(2,-2),(-2,-2),(2,0),(-2,0),(0,-2),(0,2)]
            startingNode = BinaryNode(48,48,0.5,amount=0.003,offsets=pattern)
            resArray, bestRes = runSimulations(startingNode, 5, 1, maxIteration=1000000, timeFactor=17500, probFactor=20, directory=name)
            createGif(resArray, name)
        case(6):
            # random
            name = "random" + str(random.randint(0,9000000))
            os.system("mkdir "+name)
            pattern = [(2,0),(-1,2),(2,3),(-2,-1),(0,-2)]
            startingNode = BinaryNode(48,48,0.5,amount=0.003, offsets=pattern)
            resArray, bestRes = runSimulations(startingNode, 5, 1, maxIteration=1000000, timeFactor=17500, probFactor=20, directory=name)
            createGif(resArray, name)