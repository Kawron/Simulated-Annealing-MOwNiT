import copy
import os
import random
from Node import Node
from simulatedAnnealing import *
from scipy import rand


class Sudoku(Node):

    def numToInsert(self, xOffset, yOffset):
        usedNum = []
        for i in range(3):
            for j in range(3):
                x = i + 3*xOffset
                y = j + 3*yOffset
                if self.points[y][x] != 0:
                    usedNum.append(self.points[y][x])
        newNum = []
        for i in range(1,10):
            if i not in usedNum:
                newNum.append(i)
        return newNum


    def __init__(self, points):
        self.n = 9
        self.points = points
        self.stack = []
        self.map = {}
        for i in range(9):
            for j in range(9):
                if self.points[i][j] != 0:
                    self.map[(i,j)] = self.points[i][j]


        for xOffset in range(3):
            for yOffset in range(3):
                newNum = self.numToInsert(xOffset, yOffset)
                for i in range(3):
                    for j in range(3):
                        x = i + 3*xOffset
                        y = j + 3*yOffset
                        if self.points[y][x] == 0:
                            num = newNum.pop()
                            self.points[y][x] = num

    def getEnergy(self):
        res = 0
        for i in range(self.n):
            mapa = {}
            for j in range(self.n):
                if mapa.get(self.points[i][j]) == None:
                    mapa[self.points[i][j]] = True
                else:
                    res += 1
        for i in range(self.n):
            mapa = {}
            for j in range(self.n):
                if mapa.get(self.points[j][i]) == None:
                    mapa[self.points[j][i]] = True
                else:
                    res += 1
        return res

    def neighbour(self, temp):
        while (1):
            xOffset = random.randint(0,2)
            yOffset = random.randint(0,2)

            x1 = random.randint(0,2)
            y1 = random.randint(0,2)
            x2 = random.randint(0,2)
            y2 = random.randint(0,2)

            x1 = x1 + 3*xOffset
            y1 = y1 + 3*yOffset
            x2 = x2 + 3*xOffset
            y2 = y2 + 3*yOffset

            if self.map.get((y1,x1)) == None and self.map.get((y2,x2)) == None:
                break

        self.stack.append((x1,y1,x2,y2))
        # swap
        self.points[y1][x1], self.points[y2][x2] = self.points[y2][x2], self.points[y1][x1]

    def acceptState(self):
        while self.stack != []:
            self.stack.pop()

    def prevState(self):
        while self.stack != []:
            x1,y1,x2,y2 = self.stack.pop()
            self.points[y1][x1], self.points[y2][x2] = self.points[y2][x2], self.points[y1][x1]

    def screenShot(self):
        newMatrix = copy.deepcopy(self.points)
        return newMatrix

    def newStartPoint(self):
        return self

def printRes(nodes):
    # for node in nodes:
    node = nodes[len(nodes)-1]
    n = len(node)
    for i in range(n):
        if i % 3 == 0 and i != 0:
            print("------+-------+------")
        for j in range(n):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(node[i][j], end=" ")
        print()

def run(matrix):
    name = "Sudoku" + str(random.randint(0,9000000))
    os.system("mkdir "+name)
    startingNode = Sudoku(matrix)
    print(startingNode.getEnergy())
    resArray, besRes = runSimulations(startingNode, 20, 1, maxIteration=150000, timeFactor=4000, probFactor=1, directory=name)
    printRes(resArray)

Sudoku1 = [
    [0,0,9,0,8,0,5,0,2],
    [0,0,0,0,0,0,0,0,4],
    [8,0,0,6,0,0,0,0,0],
    [0,0,0,0,0,0,0,7,0],
    [0,1,0,0,0,3,0,0,0],
    [0,0,2,0,6,0,9,0,8],
    [0,0,0,0,5,0,0,4,0],
    [0,0,7,0,0,0,0,6,0],
    [0,2,0,1,0,0,7,0,5]
]

Sudoku2 = [
    [9,0,0,0,0,8,4,0,0],
    [4,0,3,0,0,0,0,5,0],
    [0,0,0,0,7,9,2,0,0],
    [0,5,0,0,0,0,0,4,0],
    [0,0,0,6,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0],
    [3,0,7,0,0,0,0,2,0],
    [1,0,0,0,0,6,0,0,0],
    [0,0,2,0,4,5,0,8,0]
]

Sudoku3 = [
    [0,0,0,0,0,4,0,0,2],
    [6,0,0,0,0,0,0,0,0],
    [9,0,5,0,2,0,0,3,0],
    [0,0,0,8,0,0,7,0,0],
    [2,0,3,0,4,0,0,9,0],
    [0,1,0,0,0,0,0,0,0],
    [5,0,1,0,0,7,9,0,0],
    [0,6,0,0,5,0,0,0,0],
    [0,4,0,0,0,0,0,1,0]
]

def main(x):
    match(x):
        case(1):
            run(Sudoku1)
        case(2):
            run(Sudoku2)
        case(3):
            run(Sudoku3)
        case(4):
            run(matrix3)