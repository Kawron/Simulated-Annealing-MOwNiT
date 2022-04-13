import copy
import os
import random
import math
from math import sqrt
from Node import Node
from createGifZad1 import createGif
from simulatedAnnealing import previewSlope, runSimulations

def generateUni(n, width, height):
    points = []
    for _ in range(n):
        x = random.random() * width
        y = random.random() * height
        points.append((x,y))
    return points

def generateNorm(n, loc, mean):
    points = []
    for _ in range(n):
        x = random.normalvariate(loc, mean)
        y = random.normalvariate(loc, mean)
        points.append((x,y))
    return points

def generateSeperated(n, width, height):
    points = []
    sixthWidth = width/9
    sixthHeight = height/9
    groupSize = math.ceil(n/9)
    for i in range(1,9,3):
        for j in range(1,9,3):
            for _ in range(groupSize):
                x = (random.random() + i) * sixthWidth
                y = (random.random() + j) * sixthHeight
                points.append((x,y))
    return points

def seperateList(points):
    xs = [pair[0] for pair in points]
    ys = [pair[1] for pair in points]
    return xs, ys

class SalesmanNode(Node):

    def __init__(self, cities):
        self.cities = cities
        self.stack = []

    def getDist(self, a, b):
        return sqrt((b[0]-a[0])**2+(b[1]-a[1])**2)

    def getEnergy(self):
        dist = 0
        n = len(self.cities)
        for i in range(n-1):
            dist += self.getDist(self.cities[i], self.cities[i+1])
        dist += self.getDist(self.cities[0], self.cities[n-1])
        return dist

    def neighbour(self, temp):
        n = len(self.cities)
        i = random.randint(0,n-1)
        while 1:
            j = random.randint(0, n-1)
            if j != i:
                break
        self.cities[i], self.cities[j] = self.cities[j], self.cities[i]
        self.stack.append((i,j))

    def acceptState(self):
        self.stack.pop()

    def prevState(self):
        i,j = self.stack.pop()
        self.cities[i], self.cities[j] = self.cities[j], self.cities[i]

    def screenShot(self):
        newCities = copy.deepcopy(self.cities)
        return SalesmanNode(newCities)

    def newStartPoint(self):
        n = len(self.cities)
        cities = copy.deepcopy(self.cities)
        for _ in range(n*10):
            i = random.randint(0,n-1)
            while 1:
                j = random.randint(0, n-1)
                if j != i:
                    break
            cities[i], cities[j] = cities[j], cities[i]
        newNode = SalesmanNode(cities)
        return newNode

    def __str__(self):
        return str(self.cities)

def main(x):
    match x:
        case 1:
            name = "uni" + str(random.randint(0,9000000))
            os.system("mkdir "+name)

            points = generateUni(80, 100, 100)
            startingNode = SalesmanNode(points)
            # previewSlope(1000000,1,0.9,20000)
            resArray,bestRes = runSimulations(startingNode, 5, 1, maxIteration=1e6, timeFactor=30000, probFactor=8, directory=name)
            createGif(resArray, name)
        case 2:
            name = "norm" + str(random.randint(0,9000000))
            os.system("mkdir "+name)

            points = generateNorm(64, 100, 100)
            startingNode = SalesmanNode(points)
            resArray,bestRes = runSimulations(startingNode, 5, 1, maxIteration=1e6, timeFactor=30000, probFactor=8, directory=name)
            createGif(resArray, name)
        case 3:
            name = "seperated" + str(random.randint(0,9000000))
            os.system("mkdir "+name)

            points = generateSeperated(64, 100, 100)
            startingNode = SalesmanNode(points)
            resArray,bestRes = runSimulations(startingNode, 5, 1, maxIteration=1e6, timeFactor=30000, probFactor=8, directory=name)
            createGif(resArray, name)