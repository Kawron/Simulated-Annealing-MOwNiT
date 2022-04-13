from math import sqrt
import math
import random
import matplotlib.pyplot as plt

def calcTemperature(startTemp, time, alfa, timeFactor):
    Tk = startTemp*(alfa**(time/timeFactor))
    return Tk

def previewSlope(iterations, startTemp, alfa, timeFactor):
    timeArr = []
    tempArr = []
    for time in range(iterations):
        timeArr.append(time)
        tempArr.append(calcTemperature(startTemp, time, alfa, timeFactor))
    plt.plot(timeArr, tempArr)
    plt.show()


def runSimulations(startingNode, numOfRestarts, startTemp, alfa=0.9, timeFactor=500, probFactor=100, maxIteration=1e4, directory = ""):

    def probability(temp, e1, e2, probFactor):
        if e2 < e1: return 1
        return math.exp(-(abs(e2-e1))/(temp*probFactor))

    def simulatedAnnealing(startTemp, startingNode, alfa, timeFactor, probFactor, maxIteration):
        # used to display plot about cooling rate and energy levels
        timeArr = []
        tempArr = []
        energyArr=[]
        resArray = []
        
        time = 0
        temp = startTemp
        node = startingNode
        mini = float('inf')
        percentage = 0
        while time < maxIteration:
            temp = calcTemperature(startTemp, time, alfa, timeFactor)
            timeArr.append(time)
            tempArr.append(temp)

            e1 = node.getEnergy()
            node.neighbour(temp)
            e2 = node.getEnergy()
            prob = probability(temp, e1, e2, probFactor)
            
            if prob > random.random():
                node.acceptState()
            else:
                node.prevState()
            time += 1
            energyArr.append(node.getEnergy())
            
            if time % (maxIteration//126) == 0:
                resArray.append(node.screenShot())
            if time % (maxIteration//100) == 0:
                percentage += 1
                mini = min(mini, node.getEnergy())
                print(f"done: {percentage}%, temp: {temp}: energy: {node.getEnergy()} dif: {e1-e2}, prob: {prob}, time: {time}")
        resArray.append(node.screenShot())

        fig, axs = plt.subplots(2)
        axs[0].plot(timeArr, tempArr)
        axs[1].plot(timeArr, energyArr)
        print(directory + "/" + "plot.png")
        plt.savefig(directory + "/" + "plot.png")
        return resArray, node.getEnergy()

    results = []
    bestIteration = -1
    mini = float("inf")
    for i in range(numOfRestarts):
        startingNode = startingNode.newStartPoint()
        resArray, res = simulatedAnnealing(startTemp, startingNode, alfa, timeFactor, probFactor, maxIteration)
        if res < mini:
            mini = res
            bestIteration = i
        results.append(resArray)
    print(f"best res: {mini}")
    return results[bestIteration], mini